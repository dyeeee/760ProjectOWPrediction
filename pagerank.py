import numpy as np
import random
import pymysql
import pandas as pd

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

#查询match_result_2020表的所需字段数据
cur.execute("select match_id, match_winner, match_loser from match_result_2020")
result = cur.fetchall()
print(result)

df_result = pd.DataFrame(list(result),columns = ["match_id", "match_winner", "match_loser"])
print(df_result.shape)
print(df_result.head())


# # 创造数据
# # random > alpha, then here is a edge.
# def create_data(N, alpha = 0.5):
#     G = np.zeros((N, N))
#     for i in range(N):
#         for j in range(N):
#             if i == j:
#                 continue
#             if random.random() < alpha:
#                 G[i][j] = 1
#     return G
#
# G = create_data(30)
# for i in G:
#     print(i)
# #生成一个N*N的邻接矩阵，表示网页之间的链接。  等于1表示有边
#
# #GtoM:
# def GtoM(G, N):
#     M = np.zeros((N, N))     #M也是N*N的零矩阵
#     for i in range(N):
#         D_i = sum(G[i])        #一行的和
#         if D_i == 0:
#             continue
#         for j in range(N):
#             M[j][i] = G[i][j] / D_i # watch out! M_j_i instead of M_i_j
#     return M
# M = GtoM(G, 30)
#
# #Google Formula
# def PageRank(M, N, T=300, eps=1e-6, beta=0.8):
#     R = np.ones(N) / N
#     teleport = np.ones(N) / N
#     for time in range(T):
#         R_new = beta * np.dot(M, R) + (1-beta)*teleport
#         if np.linalg.norm(R_new - R) < eps:
#             break
#         R = R_new.copy()
#     return R_new
#
# values = PageRank(M, 30, T=2000)
# print(values)

