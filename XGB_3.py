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

# 2020
train_df = pd.read_table("P_Data/OWL_Data_team_match_stat_all_2020_withRank_v2.csv", sep=",")
test_df = pd.read_table("P_Data/TESTSET_P4_n7.csv", sep=",")

# split data & response
response = train_df["t1_win"]

test_Data = test_df.iloc[:, 1:]
test_response = test_df.iloc[:, 4]

# 特征选择过的
# 76,77 page
# 78,79 off
# 80,81 player

# X_train, y_train = train_df.iloc[:,
#                    [18, 19, 8, 9, 22, 23, 20, 21, 6, 7, 50, 51, 16, 17, 32, 33, 28, 29, 56, 57, 36, 37, 42, 43, 26, 27,
#                     54, 55, 68, 69, 24, 25, 76, 77]], response
# X_test, y_test = test_Data.iloc[:,
#                  [18, 19, 8, 9, 22, 23, 20, 21, 6, 7, 50, 51, 16, 17, 32, 33, 28, 29, 56, 57, 36, 37, 42, 43, 26, 27,
#                   54, 55, 68, 69, 24, 25, 76, 77]], test_response

list_index = [i for i in range(4, 76)]
list_index.append(76)
list_index.append(77)
# list_index.append(78)
# list_index.append(79)
list_index.append(80)
list_index.append(81)
X_train, y_train = train_df.iloc[:, list_index], response
X_test, y_test = test_Data.iloc[:, list_index], test_response

print("running")
# 调参
# param_grid = [{'n_estimators': range(10, 300, 10),
#                'max_depth': range(1, 10),
#                'learning_rate': [0.01, 0.1, 0.3, 0.5, 0.7]},
#               ]
# rfc = XGBClassifier(random_state=999)
#
# grid_search = GridSearchCV(rfc, param_grid, cv=3)
# grid_search.fit(X_train, y_train)
#
# print(grid_search.best_params_)
# print(grid_search.best_score_)

#
# 预测
team_2020_clf = XGBClassifier(random_state=999, n_estimators=100, max_depth=1, learning_rate=0.7)
score2 = cross_val_score(team_2020_clf, X_train, y_train, cv=10)
print("训练精度: ", score2.mean())
d = np.std(score2)
print("标准差: ", d)

model = team_2020_clf.fit(X_train, y_train)
score = cross_val_score(model, X_test, y_test, cv=10)
print("测试精度1: ", score.mean())

model = team_2020_clf.fit(X_train, y_train)
score = team_2020_clf.score(X_test, y_test)
print("测试精度2: ", score)
