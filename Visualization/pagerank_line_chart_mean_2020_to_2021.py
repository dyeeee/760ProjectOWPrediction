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


# pagerank_df = pagerank_df.iloc[49:, :].reset_index(drop=True)
# pagerank_mean_df = pagerank_df.groupby(pagerank_df.index // 3).mean()
n = 5
pagerank_df = pagerank_df.iloc[46:, :].reset_index(drop=True)
pagerank_mean_df = pagerank_df.groupby(pagerank_df.index // n).mean()

match_id_list = list(pagerank_mean_df["match_id"])
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
        y=list(pagerank_mean_df.iloc[:, i+1]),
        name=team_name_list[i],
        marker=dict(color=team_color_list[i], size=10)
    ))
layout = go.Layout(
    title=dict(text="Mean team rating 2020-2021 by Pagerank",  x=0.5),
    xaxis=dict(title=format("Round (Average of every {0} match)", str(n))),
    yaxis=dict(title="Rating"))
fig = go.Figure(data=trace0, layout=layout)
py.plot(fig, filename='pagerank_line_chart_2020_to_2021')