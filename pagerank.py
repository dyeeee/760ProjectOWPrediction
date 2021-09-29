import numpy as np
import random
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer

# 将阿杜整理的表 转化为邻接矩阵
# 链接数据库
conn = pymysql.connect(
    host = "8.129.120.114",
    port = 3306,
    user = "root",
    passwd = "123",
    db = "OWL_Data"
)

# 创建游标
cur = conn.cursor()

# 查询match_result_2020表的所需字段数据
cur.execute("select match_id, match_winner, match_loser from match_result_2020")
result = cur.fetchall()


# 原始数据 转DF格式


# 原始数据 转DF格式
# df_result = pd.DataFrame(list(result),columns = ["match_id", "match_winner", "match_loser"]).iloc[0:264,:]
# # 原始数据大小
# print("Raw data size：", df_result.shape)
# print("Raw data preview \n", df_result.tail())
#
# # df_result化为邻接矩阵
# df = pd.crosstab(df_result.match_loser, df_result.match_winner)
# print("Outcome between teams: \n", df.head())
# # idx = df.columns.union(df.index)
# # df = df.reindex(index = idx, columns = idx, fill_value=0)
#
# #这个df就是邻接矩阵了（但是现在的邻接矩阵只是有打过比赛就是1，我们要让失败方向胜利方投票，所以 df[失败方][胜利方] = 1   df[胜利方][失败方] = 0）
# #但是存在同一个队伍打过多次比赛的情况，所以   先实验让df[失败方][胜利方] 可以为1以上的数字
#
# #
# TeamName = list(df)
# print("Team Name: ", TeamName)
# Number_Team = len(TeamName)
# print("Team Number: ", Number_Team)
# G = df.values
#
#GtoM:
def GtoM(G, N):
    M = np.zeros((N, N))     #M也是N*N的零矩阵
    for i in range(N):
        D_i = sum(G[i])        #一行的和
        if D_i == 0:
            continue
        for j in range(N):
            M[j][i] = G[i][j] / D_i # 注意! 是M_j_i 而不是 M_i_j
    return M
#
#
# M = GtoM(G, Number_Team)
#
#Google Formula
def PageRank(M, N, T=300, eps=1e-6, beta=0.8):
    R = np.ones(N) / N
    teleport = np.ones(N) / N
    for time in range(T):
        R_new = beta * np.dot(M, R) + (1-beta)*teleport
        if np.linalg.norm(R_new - R) < eps:
            break
        R = R_new.copy()
    return R_new
#
# # 一维数组
# values = PageRank(M, Number_Team, T=2000)
# #字典
# pageRankResult = dict(zip(TeamName,values))
# pageRankResult = sorted(pageRankResult .items(), key=lambda item:item[1], reverse=True)
#
#
#
#
#
# print(pageRankResult)

df_result_final = pd.DataFrame(list(result),columns = ["match_id", "match_winner", "match_loser"]).iloc[0:296,:]
df_result_final["pagerank_winner"] = 0
df_result_final["pagerank_loser"] = 0
print(df_result_final[-1:])

for i in range(1,296):
    df_result = pd.DataFrame(list(result),columns = ["match_id", "match_winner", "match_loser"]).iloc[0:i,:]
    # df_result化为邻接矩阵

    # 如果不为N*N的矩阵，那么就补充上缺少的那一行/一列
    df = pd.crosstab(df_result.match_loser, df_result.match_winner)
    # 行大于列 补充winner
    if df.shape[0] > df.shape[1]:
        winner_name = list(set(list(df_result.match_loser)).difference(set(list(df_result.match_winner))))
        for q in range(0,df.shape[0]-df.shape[1]):
            df.insert(df.shape[1]-1,winner_name[q],0)



    TeamName = list(df)
    Number_Team = len(TeamName)
    G = df.values

    # 列大于行， 补充loser
    if df.shape[0] < df.shape[1]:
        for t in range(0, df.shape[1] - df.shape[0]):
            b = []
            a = []
            for j in range(0, df.shape[1]):
                a.append(0)
            b.append(a)
            G = np.append(G,b,axis=0)

    M = GtoM(G, Number_Team)
    # 一维数组
    values = PageRank(M, Number_Team, T=2000)
    # 字典
    pageRankResult = dict(zip(TeamName, values))


    # 去找下一场比赛的两支队伍
    df_nextMatch = pd.DataFrame(list(result), columns=["match_id", "match_winner", "match_loser"]).iloc[i:i+1, :]



    # 找到最后一行的两支队伍
    # pageRankResult = sorted(pageRankResult.items(), key=lambda item: item[1], reverse=True)
    # 选择出对应队伍的pagerank值，如果没有，那么就是0  存放到新的列表  pagerank_winner 和 pagerank_loser
    if df_nextMatch.iat[-1,2] in pageRankResult.keys():
        df_result_final.iloc[i, 4] = pageRankResult.get(df_nextMatch.iat[-1,2])
    else:
        df_result_final.iloc[i,4] = 0


    if df_nextMatch.iat[-1,1] in pageRankResult.keys():
        df_result_final.iloc[i, 3] = pageRankResult.get(df_nextMatch.iat[-1, 1])
    else:
        df_result_final.iloc[i, 3] = 0




print(df_result_final)


df_result_final.to_csv(r'pagerank_match_2020.csv', index=False)

