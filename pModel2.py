import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold, StratifiedKFold, RepeatedKFold
from autorank import autorank, create_report, plot_stats
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
import math

# 2020to2021
train_df = pd.read_table("FinalModel/team_match_rank_2020to2021.csv", sep=",")

# split data & response
response = train_df["t1_win"]


# 官方 78,79
# pagerank 76 77
# 选手排名 80 81
off_list = [4, 5]
team_rank = [6, 7]
player_list = [8, 9]

# 随机分
# X_train, X_test, y_train, y_test = train_test_split(train_df.iloc[96:, team_rank], response.iloc[96:], test_size=0.3,
#                                                     random_state=321)
#
# print("running")

# 手动分
X_train, y_train = train_df.iloc[0:296, team_rank+player_list], response.iloc[0:296]
X_test, y_test = train_df.iloc[296:, team_rank+player_list], response.iloc[296:]

print(X_test)
print(y_test)
# # random_state
random_state = 999

print(np.isnan(X_test).any())

# 调参数       2020是 50,150      5,8
# param_grid = [{'bootstrap': [True], 'n_estimators': range(1, 150), 'max_depth': range(1, 8)},
#               ]
# rfc = RandomForestClassifier(random_state=random_state)
#
# grid_search = GridSearchCV(rfc, param_grid, cv=3)
# grid_search.fit(X_train, y_train)
#
#
# print(grid_search.best_params_)
# print(grid_search.best_score_)


# 预测      试一下page 57 7
team_2020_rf = RandomForestClassifier(random_state=random_state, n_estimators=6, max_depth=1, bootstrap=True)

score2 = cross_val_score(team_2020_rf, X_train, y_train, cv=10)

print(score2)
print("训练精度: ", score2.mean())

d = np.std(score2)
print("标准差: ", d)


score = team_2020_rf.fit(X_train, y_train).score(X_test, y_test)
print("测试精度: ", score)

