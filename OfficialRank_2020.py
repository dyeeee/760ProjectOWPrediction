import numpy as np
import random
import pymysql
import pandas as pd

# 链接数据库
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
cur.execute("select distinct match_winner from match_result_2020 order by match_winner")
result = cur.fetchall()

# 原始数据 转DF格式
df_teamname = pd.DataFrame(list(result), columns=["team_name"])
# 原始数据大小
print("Raw data size：", df_teamname.shape)
print("Raw data preview \n", df_teamname.tail())

team_list = []
match_WL_list = []
map_WL_list = []

for index, row in df_teamname.iterrows():
    team_list.append(row['team_name'])
    match_WL_list.append(0)
    map_WL_list.append([0, 0, 0])

cur = conn.cursor()
# 查询
cur.execute("select match_id, match_winner,match_loser from match_result_2020 order by match_id")
result = cur.fetchall()

# 原始数据 转DF格式
df_match = pd.DataFrame(list(result), columns=["match_id", "match_winner", "match_loser"])

match_WL_Result_list = [["id/team", team_list]]
for index, row in df_match.iterrows():
    id = row["match_id"]
    win = row["match_winner"]
    lose = row["match_loser"]
    match_WL_list[team_list.index(win)] += 1
    match_WL_Result_list.append([id, match_WL_list.copy()])

cur = conn.cursor()
# 查询
cur.execute(
    "select match_id, map_name,map_winner,map_loser,match_winner,match_loser from match_map_result_2020 order by match_id")
result = cur.fetchall()

# 原始数据 转DF格式
df_match = pd.DataFrame(list(result), columns=["match_id", "map_name","map_winner", "map_loser", "match_winner", "match_loser"])
tmpid = 0
map_WL_Result_list = [["id/team", team_list]]
for index, row in df_match.iterrows():
    id = row["match_id"]

    if tmpid != 0:
        if tmpid != id:
            print(map_WL_list)
            map_WL_Result_list.append([tmpid, map_WL_list.copy()])
    tmpid = id

    win = row["map_winner"]
    lose = row["map_loser"]
    mwin = row["match_winner"]
    mlose = row["match_loser"]
    if win == "draw":
        map_WL_list[team_list.index(mwin)][2] += 1
        map_WL_list[team_list.index(mlose)][2] += 1
    else:
        map_WL_list[team_list.index(win)][0] += 1
        map_WL_list[team_list.index(lose)][1] += 1


print("done")
