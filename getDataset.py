import pandas as pd
import pymysql

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

cur.execute("select * from all_heroes_stat_all_2020_tmp2")
tmp2 = cur.fetchall()

tmp2 = pd.DataFrame(list(tmp2))

# 找列名
cur3 = conn.cursor()
cur3.execute("SELECT COLUMN_NAME  FROM information_schema.columns WHERE table_name='all_heroes_stat_all_2020_tmp2'")
tmp2Name = cur3.fetchall()

columnName = list(tmp2Name)
i = 0
for x in columnName:
    columnName[i] = x[0]
    i = i+1
print(columnName)

# 将列名给df
tmp2.columns = columnName


###################################
# 创建游标
cur1 = conn.cursor()

cur1.execute("select esports_match_id,team_name,player_name from all_heroes_stat_all_2020_Player")
player = cur1.fetchall()

player = pd.DataFrame(list(player))


# 将列名给df
player.columns = ['esports_match_id', 'team_name', 'player_name']

#######################################
# 创建游标
cur2 = conn.cursor()

cur2.execute("select * from playerrank_match_2020")
prank = cur2.fetchall()

prank = pd.DataFrame(list(prank))

# 找列名
cur5 = conn.cursor()
cur5.execute("SELECT COLUMN_NAME  FROM information_schema.columns WHERE table_name='playerrank_match_2020'")
prankName = cur5.fetchall()

columnName2 = list(prankName)
i = 0
for x in columnName2:
    columnName2[i] = x[0]
    i = i+1

# 将列名给df
prank.columns = columnName2

############



print(tmp2)
print(player)
print(prank)

for index, row in tmp2.iterrows():
    # print(row["team_name"])
    # 根据队名去player表中找选手名

    tn = row["team_name"]
    id1 = row["esports_match_id"]
    # player[(player.esports_match_id == id1) & (player.team_name == tn)]
    oo = player[(player.esports_match_id == id1) & (player.team_name == tn)].drop_duplicates()
    pName = list(oo.loc[:, "player_name"])
    rank = list(float(prank.loc[:, pName]))
    Arank = sum(rank)/len(pName)
    print(pName)
    print(rank)
    print(Arank)
    # prank.loc[prank.match_id == i.iat[x1, 0]] #找到了那一行
