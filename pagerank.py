import numpy as np
import random
import pymysql
import pandas as pd
import cufflinks
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go
cufflinks.go_offline(connected=True)
chart_studio.tools.set_credentials_file(username='KexiZhang', api_key='FlQ8axWch9faAuPaNzvj')

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

#原始数据 转DF格式
df_result = pd.DataFrame(list(result),columns = ["match_id", "match_winner", "match_loser"]).iloc[0:264,:]
# 原始数据大小
print("Raw data size：", df_result.shape)
print("Raw data preview \n", df_result.tail())

# df_result化为邻接矩阵
df = pd.crosstab(df_result.match_loser, df_result.match_winner)
print("Outcome between teams: \n", df.head())
# idx = df.columns.union(df.index)
# df = df.reindex(index = idx, columns = idx, fill_value=0)

#这个df就是邻接矩阵了（但是现在的邻接矩阵只是有打过比赛就是1，我们要让失败方向胜利方投票，所以 df[失败方][胜利方] = 1   df[胜利方][失败方] = 0）
#但是存在同一个队伍打过多次比赛的情况，所以   先实验让df[失败方][胜利方] 可以为1以上的数字


#
TeamName = list(df)
print("Team Name: ", TeamName)
Number_Team = len(TeamName)
print("Team Number: ", Number_Team)
G = df.values

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


M = GtoM(G, Number_Team)

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

# 一维数组
values = PageRank(M, Number_Team, T=2000)
# pageRankResult = dict(zip(TeamName, values))
# pageRankResult = dict(sorted(pageRankResult.items(), key=lambda item:item[1], reverse=True))
# print(pageRankResult)

# 战队颜色
team_color_list = ['rgb(145,15,27)',
                   'rgb(23,75,151)',
                   'rgb(255,160,0)',
                   'rgb(0,114,206)',
                   'rgb(207,70,145)',
                   'rgb(103,162,178)',
                   'rgb(251,114,153)',
                   'rgb(151,215,0)',
                   'rgb(89,203,232)',
                   'rgb(60,16,83)',
                   'rgb(255,209,0)',
                   'rgb(15,87,234)',
                   'rgb(141,4,45)',
                   'rgb(249,157,42)',
                   'rgb(165,172,175)',
                   'rgb(172,138,0)',
                   'rgb(210,38,48)',
                   'rgb(0,0,0)',
                   'rgb(47,178,40)',
                   'rgb(153,0,52)']

# 字典
pageRankResult_df = pd.DataFrame({"team_name":TeamName, "pagerank":values, "team_color":team_color_list})
print(pageRankResult_df)
pageRankResult_df = pageRankResult_df.sort_values(by="pagerank", ascending=True)

# 画图代码
trace0 = go.Bar(
    x = pageRankResult_df.pagerank,
    y = pageRankResult_df.team_name,
    orientation = 'h',
    text= pageRankResult_df.pagerank,
    marker=dict(color = pageRankResult_df.team_color)
)
layout = go.Layout(
    title = dict(text = "Team rating 2020 by Pagerank",  x = 0.5),
    xaxis = dict(title = "Rating"),
    yaxis = dict(title = "Team name"))
fig = go.Figure(data=[trace0], layout=layout)
py.plot(fig, filename = 'team_pagerank')
