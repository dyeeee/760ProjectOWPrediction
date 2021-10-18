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
cur.execute("SELECT * from match_result_2020to2021 where match_id > 37000 order by match_id")
result = cur.fetchall()
df_matchresult = pd.DataFrame(list(result), columns=["match_id", "match_winner", "match_loser"])

cur.execute("select distinct match_winner from match_result_2020to2021 order by match_winner")
result = cur.fetchall()
df_teamname = pd.DataFrame(list(result), columns=["team_name"])
team_list = ["id"]
for index, row in df_teamname.iterrows():
    team_list.append(row['team_name'])

cur.execute("SELECT * from officialrank_2021")
result = cur.fetchall()
df_officialrank = pd.DataFrame(list(result), columns=team_list)

result = {}
lastid = 0
for index, row in df_matchresult.iterrows():
    id = int(row['match_id'])
    winner = row['match_winner']
    loser = row['match_loser']
    winner_win = 0
    loser_win = 0
    if id > 37147:
        winner_win = df_officialrank[df_officialrank["id"] == lastid][winner].values[0].split(",")[0]
        loser_win = df_officialrank[df_officialrank["id"] == lastid][loser].values[0].split(",")[0]
    else:
        print("First")

    print(lastid, winner, loser, winner_win, loser_win)
    result[id] = [winner, loser, winner_win, loser_win]
    lastid = id

result_df = pd.DataFrame.from_dict(result, orient="index")
