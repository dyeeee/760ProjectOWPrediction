import pymysql
import pandas as pd


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
cur.execute("SELECT * from match_result_2020 order by match_id")
result = cur.fetchall()
df_matchresult = pd.DataFrame(list(result), columns=["match_id", "match_winner", "match_loser"])

cur.execute("select distinct match_winner from match_result_2020 order by match_winner")
result = cur.fetchall()
df_teamname = pd.DataFrame(list(result), columns=["team_name"])
team_list = []
for index, row in df_teamname.iterrows():
    team_list.append(row['team_name'])

print(team_list)