import numpy as np
import random
import pymysql
import pandas as pd

import copy

# 链接数据库
from sqlalchemy import create_engine

conn = pymysql.connect(
    host="8.129.120.114",
    port=3306,
    user="root",
    passwd="123",
    db="OWL_Data"
)

# 创建游标
cur = conn.cursor()

# 查询
cur.execute("SELECT * from match_result_2020to2021 order by match_id")
result = cur.fetchall()
df_matchresult = pd.DataFrame(list(result), columns=["match_id", "match_winner", "match_loser"])

cur.execute("select distinct match_winner from match_result_2020to2021 order by match_winner")
result = cur.fetchall()
df_teamname = pd.DataFrame(list(result), columns=["team_name"])
team_list = ["id"]
for index, row in df_teamname.iterrows():
    team_list.append(row['team_name'])

# cur.execute("select distinct player_name from player_1hour")
# result = cur.fetchall()
# df_player_name = pd.DataFrame(list(result), columns=["player_name"])
# player_name_list = ["id"]
# for index, row in df_player_name.iterrows():
#     player_name_list.append(row['player_name'])


cur.execute("SELECT * from player_rank_2020to2021 order by match_id")
des = cur.description
col = []
for i in range(len(des)):
    col.append(des[i][0])
result = cur.fetchall()
df_playerrank = pd.DataFrame(list(result), columns=col)

cur.execute("SELECT distinct esports_match_id,team_name,player_name from all_heroes_stat_all_2020to2021_Player")
result = cur.fetchall()
df_match_players = pd.DataFrame(list(result), columns=["match_id", "team_name", "player_name"])

result = {}
lastid = 0
for index, row in df_matchresult.iterrows():
    id = int(row['match_id'])
    winner = row['match_winner']
    loser = row['match_loser']
    # 找出上了谁

    q1 = "match_id=='{0}' and team_name == '{1}'".format(id, winner)
    winner_players = list(df_match_players.query(q1)["player_name"])

    q2 = "match_id=='{0}' and team_name == '{1}'".format(id, loser)
    loser_players = list(df_match_players.query(q2)["player_name"])

    winner_playrrank = 1500
    loser_playrrank = 1500
    if id > 30991:
        # 上的人的平均分
        winner_playrrank = 0
        loser_playrrank = 0
        for player in winner_players:
            q = "match_id=='{0}'".format(lastid)
            try:
                winner_playrrank += df_playerrank.query(q)[player].values[0]
                if id == 30995:
                    print(player, df_playerrank.query(q)[player].values[0])
            except:
                winner_playrrank += 1500
        winner_playrrank = winner_playrrank / len(winner_players)

        for player in loser_players:
            q = "match_id=='{0}'".format(lastid)
            try:
                loser_playrrank += df_playerrank.query(q)[player].values[0]
            except:
                loser_playrrank += 1500
        loser_playrrank = loser_playrrank / len(loser_players)
    else:
        print("First")

    print(id, winner, loser, winner_playrrank, loser_playrrank)
    result[id] = [winner, loser, winner_playrrank, loser_playrrank]
    lastid = id

result_df = pd.DataFrame.from_dict(result, orient="index")
