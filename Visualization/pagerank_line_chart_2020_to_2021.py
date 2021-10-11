import pandas as pd
import numpy as np
import csv
import cufflinks
import chart_studio
from sqlalchemy import types, create_engine
import chart_studio.plotly as py
import plotly.graph_objects as go
cufflinks.go_offline(connected=True)
chart_studio.tools.set_credentials_file(username='KexiZhang', api_key='FlQ8axWch9faAuPaNzvj')

pagerank_df = pd.read_csv("E:\Auckland\CS760 Datamining and Machine Learning\数据集\pagerank_match_allTeam_2021.csv")
#print(pagerank_df)
pagerank_df = pagerank_df.iloc[49:, :]

match_id_list = list(pagerank_df["match_id"])
new_match_id_list = list(range(len(match_id_list)))

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

team_name_list = ['Atlanta Reign', 'Boston Uprising', 'Chengdu Hunters', 'Dallas Fuel', 'Florida Mayhem', 'Guangzhou Charge', 'Hangzhou Spark', 'Houston Outlaws', 'London Spitfire', 'Los Angeles Gladiators', 'Los Angeles Valiant', 'New York Excelsior', 'Paris Eternal', 'Philadelphia Fusion', 'San Francisco Shock', 'Seoul Dynasty', 'Shanghai Dragons', 'Toronto Defiant', 'Vancouver Titans', 'Washington Justice']

trace0 = []
for i in range(20):
    trace0.append(go.Scatter(
        x=new_match_id_list,
        y=list(pagerank_df.iloc[:, i+3]),
        name=team_name_list[i],
        marker=dict(color=team_color_list[i], size=10)
    ))
layout = go.Layout(
    title=dict(text="Team rating 2020-2021 by Pagerank",  x=0.5),
    xaxis=dict(title="Match id"),
    yaxis=dict(title="Rating"))
fig = go.Figure(data=trace0, layout=layout)
py.plot(fig, filename='pagerank_line_chart_2020_to_2021')

# trace1 = []
# trace1.append(go.Scatter(
#     x=new_match_id_list,
#     y=list(pagerank_df.iloc[:, 16+3]),
#     name=team_name_list[16],
#     marker=dict(color=team_color_list[16], size=10)
# ))
# layout1 = go.Layout(
#     title=dict(text="Team rating 2020-2021 by Pagerank",  x=0.5),
#     xaxis=dict(title="Match id"),
#     yaxis=dict(title="Rating"))
# fig1 = go.Figure(data=trace1, layout=layout1)
# py.plot(fig1, filename='pagerank_line_chart_2020_to_2021_shanghai_dragon')

# # 画图代码
# team_name_list = list(pageRankResult.keys())
# team_pagerank_list = list(pageRankResult.values())
#
#
#
# trace0 = go.Bar(
#     x = team_pagerank_list,
#     y = team_name_list,
#     orientation = 'h',
#     text= team_pagerank_list,
#     marker=dict(color = team_color_list)
# )
# layout = go.Layout(
#     title = dict(text = "Team rating 2020 by Pagerank",  x = 0.5),
#     xaxis = dict(title = "Rating"),
#     yaxis = dict(title = "Team name"))
# fig = go.Figure(data=[trace0], layout=layout)
# py.plot(fig, filename = 'team_pagerank_line')

# df_player_rating = pd.DataFrame(a, columns=['player_name', 'player_rating'])
# cur.execute("select distinct player_name,role from player_role_team where player_name in (select player_name from player_total_time_played_2020)")
# role = cur.fetchall()
# df_role = pd.DataFrame(list(role), columns=["player_name", "role"])
# df_player_rating_role = pd.merge(df_player_rating, df_role)
#
# role_list = ['damage', 'tank', 'support']
# color_list = ['rgb(228,26,28)', 'rgb(55,126,184)', 'rgb(77, 175, 74)']
# symbol_list = ['triangle-up', 'circle', 'cross']
#
# trace0 = []
# for i in range(0, len(role_list)):
#     trace0.append(go.Scatter(x = [j for j in range(1, df_player_rating_role.shape[0] + 1)],
#                              y = list(df_player_rating_role[df_player_rating_role.role == role_list[i]].player_rating),
#                              mode = 'markers',
#                              text = list(df_player_rating_role[df_player_rating_role.role == role_list[i]].player_name),
#                              name = role_list[i],
#                              marker= dict(color=color_list[i], size=10, symbol = symbol_list[i])))
# layout = go.Layout(
#     title = dict(text = "Player rating 2020 by Glicko",  x = 0.5),
#     xaxis = dict(title = "Ranking"),
#     yaxis = dict(title = "Player rating"))
# fig = go.Figure(data=trace0, layout=layout)
# py.plot(fig, filename = 'player_rating_role')