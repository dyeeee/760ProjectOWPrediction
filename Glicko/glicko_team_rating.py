import glicko2
import pymysql
import pandas as pd

class TeamRating(object):

    def __init__(self, df_result):
        self._result = df_result
        self._rate = dict()

    def InitTeams(self):
        for team in self._result['match_winner']:
            if team not in self._rate:
                self._rate[team] = glicko2.Player()
        for team in self._result['match_loser']:
            if team not in self._rate:
                self._rate[team] = glicko2.Player()

    def CalcualteRate(self):
        self.InitTeams()
        for _, outcome in self._result.iterrows():
            winner = self._rate[outcome[1]]
            loser = self._rate[outcome[2]]
            loser_rating = loser.rating
            loser_rd = loser.rd
            loser.update_player([winner.rating], [winner.rd], [0])
            winner.update_player([loser_rating], [loser_rd], [1])

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
    result = cur.fetchall()

    df_result = pd.DataFrame(list(result), columns=["match_id", "match_winner", "match_loser"])

    TR = TeamRating(df_result)
    TR.CalcualteRate()
    for team in sorted (TR._rate):
        print(str(team) + "\t" + str(TR._rate[team].rating))
    print(sorted(TR._rate.items(), key=lambda kv: (kv[1], kv[0])))

