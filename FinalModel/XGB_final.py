import xgboost as xgb
from xgboost import plot_importance
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import warnings
from xgboost.sklearn import XGBClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV

random_state = 9999

# 2020to2021
train_df = pd.read_table("../FinalModel/team_match_rank_2020to2021.csv", sep=",")

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

print("running")

# 调参
# param_grid = [{'n_estimators': range(1, 50),
#                'max_depth': range(1, 10),
#                'learning_rate': [0.01, 0.1, 0.3, 0.5, 0.7]},
#               ]
# rfc = XGBClassifier(random_state=random_state)
#
# grid_search = GridSearchCV(rfc, param_grid, cv=3)
# grid_search.fit(X_train, y_train)
#
# print(grid_search.best_params_)
# print(grid_search.best_score_)

#
# 预测
team_2020_clf = XGBClassifier(random_state=random_state,
                              n_estimators=21, max_depth=4, learning_rate=0.5)
score2 = cross_val_score(team_2020_clf, X_train, y_train, cv=10)
print("训练精度: ", score2.mean())
d = np.std(score2)
print("标准差: ", d)

model = team_2020_clf.fit(X_train, y_train)
score = team_2020_clf.score(X_test, y_test)
print("测试精度: ", score)
