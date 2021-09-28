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
cur.execute("select distinct match_winner from match_result_2020 order by match_winner")
result = cur.fetchall()
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
    map_WL_list.append([0, 0, 0, 0])

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
df_match = pd.DataFrame(list(result),
                        columns=["match_id", "map_name", "map_winner", "map_loser", "match_winner", "match_loser"])
tmpid = 0
colname = [team_list]
map_WL_Result_list = []
for index, row in df_match.iterrows():
    id = row["match_id"]

    if tmpid != 0:
        if tmpid != id:
            map_WL_list[team_list.index(lastMwin)][0] += 1
            map_WL_Result_list.append([tmpid, copy.deepcopy(map_WL_list)])
    tmpid = id

    win = row["map_winner"]
    lose = row["map_loser"]
    mwin = row["match_winner"]
    mlose = row["match_loser"]
    if win == "draw":
        map_WL_list[team_list.index(mwin)][3] += 1
        map_WL_list[team_list.index(mlose)][3] += 1
    else:
        map_WL_list[team_list.index(win)][1] += 1
        map_WL_list[team_list.index(lose)][2] += 1
    lastMwin = row["match_winner"]

print("done")

result_dict = {}
tmp = pd.DataFrame(result_dict)
for item in map_WL_Result_list:
    result_dict[item[0]] = item[1]

tmp = pd.DataFrame(result_dict)
result = pd.DataFrame(tmp.values.T, index=tmp.columns, columns=tmp.index)
result.columns = colname
result = result.applymap(lambda x: ", ".join(list(map(str, x))))

# cur.execute("drop table if exists officialrank_match_2020")  # 以重新写入的方式导入数据表
# connect = create_engine("mysql+pymysql://root:123@8.129.120.114:3306/OWL_Data?charset=utf8")
# pd.io.sql.to_sql(result, "officialrank_match_2020", connect, schema="OWL_Data", index=False, if_exists="append")
