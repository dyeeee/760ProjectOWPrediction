from plotly.graph_objs import Figure

import glicko2
import pymysql
import pandas as pd
import numpy as np
import cufflinks
import chart_studio
from sqlalchemy import types, create_engine
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
        self.blacklist = ["ta1yo", "ryujehong", "Geguri", "sayaplayer", "Munchkin", "Ado", "mikeyy", "ColdesT", "Bischu", "ChipSa", "LeeJaegon", "Luffy", "HyP", "Farway1987"]

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

            if data[4] < 100:
                continue

            if(matchId not in self._matchDict):
                self._matchDict[matchId] = dict()
            if(playerName not in self._matchDict[matchId]): #队名， 时间, 数据1：13
                self._matchDict[matchId][playerName] = list([data[3], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

            self._matchDict[matchId][playerName][1] += float(data[4]) #time_played
            self._matchDict[matchId][playerName][2] += float(data[5])
            self._matchDict[matchId][playerName][3] += float(data[6])
            self._matchDict[matchId][playerName][4] += float(data[7])
            self._matchDict[matchId][playerName][5] += float(data[8])
            self._matchDict[matchId][playerName][6] += float(data[9])
            self._matchDict[matchId][playerName][7] += float(data[10])
            self._matchDict[matchId][playerName][8] += float(data[11])
            self._matchDict[matchId][playerName][9] += float(data[12])
            self._matchDict[matchId][playerName][10] += float(data[13])
            self._matchDict[matchId][playerName][11] += float(data[14])
            self._matchDict[matchId][playerName][12] += float(data[15])
            self._matchDict[matchId][playerName][13] += float(data[16])
            self._matchDict[matchId][playerName][14] += float(data[17])
            #self.playtime[playerName] += float(data[4])

    def InitNorm(self):
        elim = list()
        hdd = list()
        oa = list()
        uef = list()
        uu = list()
        da = list()
        hd = list()
        dbg = list()
        hbg = list()
        nba = list()
        nbe = list()
        sdh = list()
        sdsr = list()
        for match in self._matchDict.values():
            for player in match.values():
                elim.append(player[2]/player[1])
                hdd.append(player[3]/player[1])
                oa.append(player[4]/player[1])
                uef.append(player[5]/player[1])
                uu.append(player[6]/player[1])
                da.append(player[7]/player[1])
                hd.append(player[8]/player[1])
                dbg.append(player[9]/player[1])
                hbg.append(player[10]/player[1])
                nba.append(player[11]/player[1])
                nbe.append(player[12]/player[1])
                sdh.append(player[13]/player[1])
                sdsr.append(player[14]/player[1])

        self._zscore["Eliminations"] = list([np.average(elim), np.std(elim)])
        self._zscore["HeroDamageDone"] = list([np.average(hdd), np.std(hdd)])
        self._zscore["OffensiveAssists"] = list([np.average(oa), np.std(oa)])
        self._zscore["UltimateEarned"] = list([np.average(uef), np.std(uef)])
        self._zscore["UltimateUsed"] = list([np.average(uu), np.std(uu)])
        self._zscore["DefensiveAssists"] = list([np.average(da), np.std(da)])
        self._zscore["HealingDone"] = list([np.average(hd), np.std(hd)])
        self._zscore["DamageBioticGrenade"] = list([np.average(dbg), np.std(dbg)])
        self._zscore["HealdingBioticGrenade"] = list([np.average(hbg), np.std(hbg)])
        self._zscore["NanoBoostAssists"] = list([np.average(nba), np.std(nba)])
        self._zscore["NanoBoostEfficiency"] = list([np.average(nbe), np.std(nbe)])
        self._zscore["SleepDartHits"] = list([np.average(sdh), np.std(sdh)])
        self._zscore["SleepDartSuccessRate"] = list([np.average(sdsr), np.std(sdsr)])


    def DpsNormalization(self, inf):
        elim = (inf[2]/inf[1] - self._zscore["Eliminations"][0]) / self._zscore["Eliminations"][1]
        hdd = (inf[3]/inf[1] - self._zscore["HeroDamageDone"][0]) / self._zscore["HeroDamageDone"][1]
        oa = (inf[4]/inf[1] - self._zscore["OffensiveAssists"][0]) / self._zscore["OffensiveAssists"][1]
        uef = (inf[5]/inf[1] - self._zscore["UltimateEarned"][0]) / self._zscore["UltimateEarned"][1]
        uu = (inf[6]/inf[1] - self._zscore["UltimateUsed"][0]) / self._zscore["UltimateUsed"][1]
        da = (inf[7]/inf[1] - self._zscore["DefensiveAssists"][0]) / self._zscore["DefensiveAssists"][1]
        hd = (inf[8]/inf[1] - self._zscore["HealingDone"][0]) / self._zscore["HealingDone"][1]
        dbg = (inf[9]/inf[1] - self._zscore["DamageBioticGrenade"][0]) / self._zscore["DamageBioticGrenade"][1]
        hbg = (inf[10]/inf[1] - self._zscore["HealdingBioticGrenade"][0]) / self._zscore["HealdingBioticGrenade"][1]
        nba = (inf[11]/inf[1] - self._zscore["NanoBoostAssists"][0]) / self._zscore["NanoBoostAssists"][1]
        nbe = (inf[12]/inf[1] - self._zscore["NanoBoostEfficiency"][0]) / self._zscore["NanoBoostEfficiency"][1]
        sdh = (inf[13]/inf[1] - self._zscore["SleepDartHits"][0]) / self._zscore["SleepDartHits"][1]
        sdsr = (inf[14]/inf[1] - self._zscore["SleepDartSuccessRate"][0]) / self._zscore["SleepDartSuccessRate"][1]

        per = (elim + hdd + oa + uef + uu + da + hd + dbg + hbg + nba + nbe + sdh + sdsr) / 13
        return per


    def CalcualteRate(self):
        self.InitTeams()
        self.InitPlayers()
        self.InitmatchDict()
        self.InitNorm()

        performance = []

        for _, outcome in self._result.iterrows():
            matchId = outcome[0]
            winner = self._teamrate[outcome[1]]
            loser = self._teamrate[outcome[2]]
            loser_rating = loser.rating
            loser_rd = loser.rd
            winner_rating = winner.rating
            winner_rd = winner.rd

            if(matchId not in self._matchDict):
                continue
            for player, inf in self._matchDict[matchId].items():
                playerRate = self._playerRate[player]
                normDps =  self.DpsNormalization(inf)

                normDps = (normDps + 1.5) / 10
                performance.append(normDps)

                if(outcome[1] == inf[0]):
                    playerRate.update_player([loser_rating], [loser_rd], [1 + normDps])
                else:
                    playerRate.update_player([winner_rating], [winner_rd], [normDps])

            loser.update_player([winner_rating], [winner_rd], [0])
            winner.update_player([loser_rating], [loser_rd], [1])

            for player, rate in self._playerRate.items():
                self.rateRealtime[player][matchId] = rate.rating
        print(max(performance), min(performance))





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
    cur.execute("select match_id, match_winner, match_loser from match_result_2020to2021")
    df_match_result = cur.fetchall()

    df_result = pd.DataFrame(list(df_match_result), columns=["match_id", "match_winner", "match_loser"])

    cur.execute("select esports_match_id, player_name, team_name, `Time Played`, Eliminations, `Hero Damage Done`\
                , `Offensive Assists`, `Ultimates Earned - Fractional`, `Ultimates Used`, `Defensive Assists`, `Healing Done`\
                , `Damage - Biotic Grenade`, `Healing - Biotic Grenade`, `Nano Boost Assists`, `Nano Boost Efficiency`, `Sleep Dart Hits`, `Sleep Dart Success Rate`\
                from ana_stat_all_2020to2021_Player")
    hero = cur.fetchall()
    df_hero = pd.DataFrame(list(hero), columns=["match_id", "player_name", "team_name", "time_played", "Eliminations"
                                                , "Hero Damage Done", "Offensive Assists", "Ultimates Earned - Fractional", "Ultimates Used"
                                                , "Defensive Assists", "Healing Done", "Damage - Biotic Grenade", "Healing - Biotic Grenade"
                                                , "Nano Boost Assists", "Nano Boost Efficiency", "Sleep Dart Hits", "Sleep Dart Success Rate"])

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
        if(player[1] == 1500):
            continue
        print(str(i) + "\t" + str(player[0]) + "\t" + str(player[1]))
        # 0 is player name, 1 is player rating
        i+=1

    data = pd.DataFrame(TR.rateRealtime)
    data.index.name = 'match_id'
    # connect = create_engine("mysql+pymysql://root:123@8.129.120.114:3306/OWL_Data?charset=utf8")
    #
    # data.to_sql('player_rating_in_realTime', connect, if_exists = 'replace', dtype={'match_id', types.Integer})

    #画图代码
    #combine player_rating and their role

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
    #     title = dict(text = "Player rating 2020 by Glicko",  x = 0.5),
    #     xaxis = dict(title = "Ranking"),
    #     yaxis = dict(title = "Player rating"))
    # fig = go.Figure(data=trace0, layout=layout)
    # py.plot(fig, filename = 'player_rating_role')
    #
    # cur.close()


