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
        self._zscore = dict()

        self.playtime = dict()
        self.blacklist = ["ta1yo", "ryujehong", "Geguri", "sayaplayer", "Munchkin", "Ado", "mikeyy", "ColdesT", "Bischu", "ChipSa"]

        self.rateRealtime = dict()

    def InitTeams(self):
        for team in self._result['match_winner']:
            if team not in self._teamrate:
                self._teamrate[team] = glicko2.Player()
        for team in self._result['match_loser']:
            if team not in self._teamrate:
                self._teamrate[team] = glicko2.Player()

    def InitPlayers(self):
        for player in self._heros['player_name']:
            if(player in self.blacklist):
                continue
            if(player not in self._playerRate):
                self._playerRate[player] = glicko2.Player()
            if(player not in self.playtime):
                self.playtime[player] = 0
            if(player not in self.rateRealtime):
                self.rateRealtime[player] = dict();

    def InitmatchDict(self):
        for data in self._heros.itertuples():
            matchId = data[1]
            playerName = data[2]

            if playerName in self.blacklist:
                continue

            if(matchId not in self._matchDict):
                self._matchDict[matchId] = dict()
            if(playerName not in self._matchDict[matchId]): #队名， 数据1,2,3,4,5,6, 时间
                self._matchDict[matchId][playerName] = list([data[3], 0, 0, 0, 0, 0, 0, 0, 0])

            self._matchDict[matchId][playerName][1] += float(data[5])
            self._matchDict[matchId][playerName][2] += float(data[6])
            self._matchDict[matchId][playerName][3] += float(data[7])
            self._matchDict[matchId][playerName][4] += float(data[8])
            self._matchDict[matchId][playerName][5] += float(data[9])
            self._matchDict[matchId][playerName][6] += float(data[10])
            self._matchDict[matchId][playerName][7] += float(data[11])
            self._matchDict[matchId][playerName][8] += float(data[4])
            self.playtime[playerName] += float(data[4])

    def InitNorm(self):
        assists = list()
        ata = list()
        deaths = list()
        fb = list()
        ek = list()
        mp = list()
        hd = list()
        for match in self._matchDict.values():
            for player in match.values():
                assists.append(player[1]/player[8])
                ata.append(player[2]/player[8])
                deaths.append(player[3]/player[8])
                fb.append(player[4]/player[8])
                ek.append(player[5]/player[8])
                mp.append(player[6]/player[8])
                hd.append(player[7]/player[8])

        self._zscore["Assist"] = list([np.average(assists), np.std(assists)])
        self._zscore["TimeAlive"] = list([np.average(ata), np.std(ata)])
        self._zscore["Deaths"] = list([np.average(deaths), np.std(deaths)])
        self._zscore["FinalBlows"] = list([np.average(fb), np.std(fb)])
        self._zscore["Environment"] = list([np.average(ek), np.std(ek)])
        self._zscore["Melee"] = list([np.average(mp), np.std(mp)])
        self._zscore["HealingDone"] = list([np.average(hd), np.std(hd)])


    def DpsNormalization(self, inf):
        assist = (inf[1]/inf[8] - self._zscore["Assist"][0]) / self._zscore["Assist"][1]
        ta = (inf[2]/inf[8] - self._zscore["TimeAlive"][0]) / self._zscore["TimeAlive"][1]
        death = inf[3]/inf[8] - self._zscore["Deaths"][0] / self._zscore["Deaths"][1]
        fb = (inf[4]/inf[8] - self._zscore["FinalBlows"][0]) / self._zscore["FinalBlows"][1]
        ek = (inf[5]/inf[8] - self._zscore["Environment"][0]) / self._zscore["Environment"][1]
        mp = (inf[6]/inf[8] - self._zscore["Melee"][0]) / self._zscore["Melee"][1]
        hd = (inf[7]/inf[8] - self._zscore["HealingDone"][0]) / self._zscore["HealingDone"][1]


        per = (assist + ta + fb + ek + mp - death + hd) / 7
        return per


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

            for player, inf in self._matchDict[matchId].items():
                playerRate = self._playerRate[player]
                normDps =  self.DpsNormalization(inf)
                if(winner == inf[0]):
                    playerRate.update_player([loser_rating], [loser_rd], [1 + normDps])
                else:
                    playerRate.update_player([winner_rating], [winner_rd], [normDps])

            loser.update_player([winner_rating], [winner_rd], [0])
            winner.update_player([loser_rating], [loser_rd], [1])

            for player, rate in self._playerRate.items():
                self.rateRealtime[player][matchId] = rate.rating





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
    df_match_result = cur.fetchall()

    df_result = pd.DataFrame(list(df_match_result), columns=["match_id", "match_winner", "match_loser"])

    cur.execute("select esports_match_id, player_name, team_name, `Time Played`, Assists, `Average Time Alive`\
                , Deaths, `Final Blows`, `Environmental Kills`, `Melee Percentage of Final Blows`, `Healing Done`\
                from all_heroes_stat_all_2020_Player")
    hero = cur.fetchall()
    df_hero = pd.DataFrame(list(hero), columns=["match_id", "player_name", "team_name", "time_played", "Assists"
                                                , "Average Time Alive", "Deaths", "Final Blows", "Environmental Kills"
                                                , "Melee Percentage of Final Blows", "Healing Done"])

    cur.execute("select player_name, role from player_role_team")
    role = cur.fetchall()
    df_player_role = pd.DataFrame(list(role), columns=["player_name", "role"])

    TR = PlayerRating(df_result, df_hero)
    TR.CalcualteRate()
    a = list()
    for player in sorted (TR._playerRate):
        a.append((player, TR._playerRate[player].rating))
        # print(str(team) + "\t" + str(TR._rate[team].rating))
    a.sort(key = takeSecond, reverse=True)
    i = 1
    for player in a:
        print(str(i) + "\t" + str(player[0]) + "\t" + str(player[1]))
        # 0 is player name, 1 is player rating
        i+=1

    data = pd.DataFrame(TR.rateRealtime)
    print()

    # 画图代码
    # combine player_rating and their role

    # df_player_rating = pd.DataFrame(a, columns=['player_name', 'player_rating'])
    # cur.execute("select distinct player_name,role from player_role_team where player_name in (select player_name from player_total_time_played_2020)")
    # role = cur.fetchall()
    # df_role = pd.DataFrame(list(role), columns=["player_name", "role"])
    # df_player_rating_role = pd.merge(df_player_rating, df_role)
    #
    # role_list = ['damage', 'tank', 'support']
    # color_list = ['rgb(228,26,28)', 'rgb(55,126,184)', 'rgb(77, 175, 74)']
    # symbol_list = ['triangle-up', 'circle', 'cross']
    #
    # trace0 = []
    # for i in range(0, len(role_list)):
    #     trace0.append(go.Scatter(x = [j for j in range(1, df_player_rating_role.shape[0] + 1)],
    #                              y = list(df_player_rating_role[df_player_rating_role.role == role_list[i]].player_rating),
    #                              mode = 'markers',
    #                              text = list(df_player_rating_role[df_player_rating_role.role == role_list[i]].player_name),
    #                              name = role_list[i],
    #                              marker= dict(color=color_list[i], size=10, symbol = symbol_list[i])))
    # layout = go.Layout(
    #     title = dict(text = "Player rating demo 2020 by Glicko",  x = 0.5),
    #     xaxis = dict(title = "Ranking"),
    #     yaxis = dict(title = "Player rating"))
    # fig = go.Figure(data=trace0, layout=layout)
    # py.plot(fig, filename = 'player_rating_role')


