# import xgboost as xgb
# from xgboost import plot_importance
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import warnings

from sklearn.model_selection import GridSearchCV
#
from sklearn import metrics
from sklearn.svm import SVC

seed = 7
np.random.seed(seed)

df = pd.read_table("OWL_Data_team_match_stat_all_2020_withRank_v3.csv", sep=",")
test_df = pd.read_table("OWL_Data_TESTSET_V3.csv", sep=",")

new_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14]
off_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14, 40]
pag_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14, 41]
pr_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14, 42]
add_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14, 41, 42]

data = df.iloc[:, new_index]
response = df["t1_win"]

test_Data = test_df.iloc[:, new_index]
test_response = test_df["t1_win"]

X_train, y_train = data, response
X_test, y_test = test_Data, test_response


# 调参
# param_grid = [{'bootstrap': [True], 'n_estimators': range(1, 150), 'max_depth': range(1, 8)},
#               ]
# rfc = RandomForestClassifier(random_state=999)
#
# grid_search = GridSearchCV(rfc, param_grid, cv=3)
# grid_search.fit(X_train, y_train)
#
#
# print(grid_search.best_params_)
# print(grid_search.best_score_)


# 预测
team_2020_rf = RandomForestClassifier(random_state=999, n_estimators=58, max_depth=2, bootstrap=True)
score = cross_val_score(team_2020_rf, X_test, y_test, cv=10)
score2 = cross_val_score(team_2020_rf, X_train, y_train, cv=10)
print("测试精度: ", score.mean())
print("训练精度: ", score2.mean())
d = np.std(score)

print("标准差: ", d)




