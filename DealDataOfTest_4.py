import numpy as np
import random
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

# 查询match_result_2020表的所需字段数据
cur.execute("select * from team_match_stat_all_2020_withRank")
result = cur.fetchall()

# 原始数据 转DF格式
df_result = pd.DataFrame(list(result))

# 原始数据大小
print("Raw data size：", df_result.shape)
print("Raw data preview \n", df_result.iloc[:, [num for num in range(4, 82)]])

flist = [num for num in range(4, 82)]

# 遍历所有team1 找比赛id小于它的 名字等于它的比赛
# 如果比赛数大于5，那么就取 id最大的五场，否则就选择全部  如果没有比赛，先都设为0吧

p = df_result.copy(deep=True)

for i in range(df_result.shape[0]):
    q = df_result[(df_result.iloc[:, 1] == df_result.iloc[i, 1]) & (df_result.iloc[:, 0] < df_result.iloc[i, 0])]
    if q.shape[0] == 0:
        p.iloc[i, flist] = [0 for _ in range(4, 82)]
        print(p.iloc[i, 1], "之前没有比赛")
    elif q.shape[0] < 5:
        # 小于5场，设置为他们所有的和的均值
        q = q.sort_values(by=0, axis=0, ascending=False)
        # print(q, i, q.shape[0])
        p.iloc[i, flist] = q.iloc[0:q.shape[0], flist].mean()
        # print(q.iloc[0:q.shape[0], [3, 4, 5, 6]].mean().T)
    else:
        # 选取前五场
        q = q.sort_values(by=0, axis=0, ascending=False)

        p.iloc[i, flist].update(q.iloc[0:5, flist].mean())

pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# print(p.iloc[:, [0, 2, 3, 4, 5, 6]])

# 一句话
# x = df_result[(df_result.iloc[:,2] == "Vancouver Titans") & (df_result.iloc[:,0].astype(int) < 34811)]
# x = x.sort_values(by=0, axis=0,  ascending=False)
# print(x.iloc[:,[3, 4]])
# o  = x.iloc[0:5, [3, 4, 5, 6]].mean()
# print(pd.DataFrame(o).T)
