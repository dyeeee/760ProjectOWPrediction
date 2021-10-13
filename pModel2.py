import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold, StratifiedKFold, RepeatedKFold
from autorank import autorank, create_report, plot_stats
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV

# train_df = pd.read_table("OWL_Data_team_match_stat_all_2020_withRank_v3.csv", sep=",")
# test_df = pd.read_table("OWL_Data_TESTSET_V3.csv", sep=",")

# 2021
# train_df = pd.read_table("P_Data/OWL_Data_team_match_stat_all_2020to2021.csv", sep=",")
# test_df = pd.read_table("P_Data/TESTSET_v4_n3.csv", sep=",")

# 2020
train_df = pd.read_table("P_Data/OWL_Data_team_match_stat_all_2020_withRank_v2.csv", sep=",")
test_df = pd.read_table("P_Data/TESTSET_P4_n5.csv", sep=",")


# split data & response
response = train_df["t1_win"]

test_Data = test_df.iloc[:, 1:]
test_response = test_df.iloc[:, 4]

# 特征选择过的
X_train, y_train = train_df.iloc[:, [18,19,8,9,22,23,20,21,6,7,50,51,16,17,32,33,28,29,56,57,36,37,42,43,26,27,54,55,68,69,24,25,76,77]], response
X_test, y_test = test_Data.iloc[:, [18,19,8,9,22,23,20,21,6,7,50,51,16,17,32,33,28,29,56,57,36,37,42,43,26,27,54,55,68,69,24,25,76,77]], test_response

# 没有特征选择过
# list1 = [i for i in range(4, 78)]
# list1.append(80)
# list1.append(81)
#
# X_train, y_train = train_df.iloc[:, list1], response
# X_test, y_test = test_Data.iloc[:, list1], test_response


# # random_state
random_state = 999
# # 随机森林models
# # 随机森林主要的参数有n_estimators（子树的数量）、max_depth（树的最大生长深度）、min_samples_leaf（叶子的最小样本数量）
# # min_samples_split(分支节点的最小样本数量）、max_features（最大选择特征数）
#



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
team_2020_rf = RandomForestClassifier(random_state=random_state, n_estimators=52, max_depth=5, bootstrap=True)

score2 = cross_val_score(team_2020_rf, X_train, y_train, cv=10)

print("训练精度: ", score2.mean())
d = np.std(score2)
print("标准差: ", d)


score = team_2020_rf.fit(X_train, y_train).score(X_test, y_test)
print("测试精度: ", score)

model = team_2020_rf.fit(X_train, y_train)

score3 = cross_val_score(model, X_test, y_test, cv=10)
print(score3.mean())
