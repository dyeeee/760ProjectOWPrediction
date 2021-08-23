from plotly.graph_objs import Figure

import glicko2
import pymysql
import pandas as pd
import numpy as np
import cufflinks
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go
cufflinks.go_offline(connected=True)
chart_studio.tools.set_credentials_file(username='KexiZhang', api_key='FlQ8axWch9faAuPaNzvj')


class PlayerRating(object):

    def __init__(self, df_result, df_heros):
        self._result = df_result
        self._heros = df_heros
        self._teamrate = dict()
        self._playerRate = dict()
        self._matchDict = dict()
        self._zscore = list()

    def InitTeams(self):
        for team in self._result['match_winner']:
            if team not in self._teamrate:
                self._teamrate[team] = glicko2.Player()
        for team in self._result['match_loser']:
            if team not in self._teamrate:
                self._teamrate[team] = glicko2.Player()

    def InitPlayers(self):
        for player in self._heros['player_name']:
            if(player not in self._playerRate):
                self._playerRate[player] = glicko2.Player()

    def InitmatchDict(self):
        for data in self._heros.itertuples():
            matchId = data[1]
            playerName = data[2]
            if(matchId not in self._matchDict):
                self._matchDict[matchId] = dict()
            if(playerName not in self._matchDict[matchId]):
                self._matchDict[matchId][playerName] = list([data[3], 0, 0])
            self._matchDict[matchId][playerName][1] += float(data[4])
            self._matchDict[matchId][playerName][2] += float(data[5])

    def InitNorm(self):
        dps = list()
        for match in self._matchDict.values():
            for player in match.values():
                dps.append(player[1]/player[2])
        self._zscore.append(np.average(dps))
        self._zscore.append(np.std(dps))

    def DpsNormalization(self, dps):
        return (dps - self._zscore[0])/self._zscore[1]


    def CalcualteRate(self):
        self.InitTeams()
        self.InitPlayers()
        self.InitmatchDict()
        self.InitNorm()
        for _, outcome in self._result.iterrows():
            matchId = outcome[0]
            winner = self._teamrate[outcome[1]]
            loser = self._teamrate[outcome[2]]
            loser_rating = loser.rating
            loser_rd = loser.rd
            winner_rating = winner.rating
            winner_rd = winner.rd

            if(int(matchId) == 34844):
                return

            for player, inf in self._matchDict[matchId].items():
                playerRate = self._playerRate[player]
                normDps =  self.DpsNormalization(inf[1]/inf[2])
                if(winner == inf[0]):
                    playerRate.update_player([loser_rating], [loser_rd], [1 + normDps])
                else:
                    playerRate.update_player([winner_rating], [winner_rd], [normDps])



            loser.update_player([winner_rating], [winner_rd], [0])
            winner.update_player([loser_rating], [loser_rd], [1])

def takeSecond(elem):
    return elem[1]

if __name__ == '__main__':
    conn = pymysql.connect(
        host="8.129.120.114",
        port=3306,
        user="root",
        passwd="123",
        db="OWL_Data"
    )
    cur = conn.cursor()
    cur.execute("select match_id, match_winner, match_loser from match_result_2020")
    df_player_rating_role = cur.fetchall()

    df_result = pd.DataFrame(list(df_player_rating_role), columns=["match_id", "match_winner", "match_loser"])

    cur.execute("select esports_match_id, player_name, team_name, stat_amount, time_played from all_heroes_damage_2020_1")
    hero = cur.fetchall()
    df_hero = pd.DataFrame(list(hero), columns=["match_id", "player_name", "team_name", "damage_amount", "time_played"])



    TR = PlayerRating(df_result, df_hero)
    TR.CalcualteRate()
    a = list()
    for player in sorted (TR._playerRate):
        a.append((player, TR._playerRate[player].rating))
        # print(str(team) + "\t" + str(TR._rate[team].rating))
    a.sort(key = takeSecond, reverse=True)
    i = 1
    # for player in a:
    #     print(str(i) + "\t" + str(player[0]) + "\t" + str(player[1]))
    #     # 0 is player name, 1 is player rating
    #     i+=1

    # combine player_rating and their role
    df_player_rating = pd.DataFrame(a, columns=['player_name', 'player_rating'])
    # print(df_player_rating)
    cur.execute("select distinct player_name,role from player_role_team")
    role = cur.fetchall()
    df_role = pd.DataFrame(list(role), columns=["player_name", "role"])
    df_player_rating_role = pd.merge(df_player_rating, df_role)

    role_set = ['damage', 'tank', 'support']
    color_set = ['rgb(228,26,28)', 'rgb(55,126,184)', 'rgb(77, 175, 74)']
    symbol_set = ['triangle-up', 'circle', 'cross']

    trace0 = []
    for i in range(0, len(role_set)):
        trace0.append(go.Scatter(x = [j for j in range(1, df_player_rating_role.shape[0] + 1)],
                                 y = list(df_player_rating_role[df_player_rating_role.role == role_set[i]].player_rating),
                                 mode = 'markers',
                                 text = list(df_player_rating_role[df_player_rating_role.role == role_set[i]].player_name),
                                 name = role_set[i],
                                 marker= dict(color=color_set[i], size=10, symbol = symbol_set[i])))
    layout = go.Layout(
        title = dict(text = "Player rating by Glicko",  x = 0.5),

        xaxis = dict(title = "Ranking"),
        yaxis = dict(title = "Player rating"))
    fig = go.Figure(data=trace0, layout=layout)
    py.plot(fig, filename = 'player_rating_role')
    #py.plot(trace0, filename='player_rating_role')


