import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold, StratifiedKFold, RepeatedKFold
from autorank import autorank, create_report, plot_stats
# from xgboost import XGBClassifier
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV


df = pd.read_table("./Subdata/team_match_stat_2020.csv", sep=",")
test_df = pd.read_table("./Subdata/TEST_team_match_stat_2020.csv", sep=",")

# split data & response
data = df.iloc[:, 2:]
response = df["t1_win"]

test_Data = test_df.iloc[:, 2:]
test_response = test_df["t1_win"]

X_train, y_train = data, response
X_va, y_va = test_Data.iloc[0:100], test_response.iloc[0:100]
X_test, y_test = test_Data.iloc[101:282], test_response.iloc[101:282]



# 4. Modeling by repeated-cross-validation
model_names = ["RF", "Ada", "Bagging", "XGB"]
model_names_index = 0
team_2020_scores_df = pd.DataFrame()

# random_state
random_state = 999
# 随机森林models
# 随机森林主要的参数有n_estimators（子树的数量）、max_depth（树的最大生长深度）、min_samples_leaf（叶子的最小样本数量）
# min_samples_split(分支节点的最小样本数量）、max_features（最大选择特征数）

team_2020_rf = RandomForestClassifier(random_state=random_state, n_estimators=10)
print(team_2020_rf.fit(X_train, y_train).score(X_test, y_test))
# n_estimators是影响最大的，所以先调n_estimators

# 调参，绘制学习曲线来调参n_estimators
score_lt = []

# 每隔10步就建立一个随机森林，获得不同的n_estimators得分
for i in range(0, 200, 10):
    rfc = RandomForestClassifier(n_estimators=i+1, random_state=random_state)
    score = rfc.fit(X_train, y_train).score(X_va, y_va)
    score_lt.append(score)

score_max = max(score_lt)
print(score_lt)
print('最大得分：{}'.format(score_max),
      '子树数量为：{}'.format(score_lt.index(score_max)*10+1))



# x = np.arange(1, 201, 10)
# plt.subplot(111)
# plt.plot(x, score_lt, 'r-')
# plt.show()

# 找到最好的参数的位置，进行进一步细分
max_n = score_lt.index(score_max)*10+1
for i in range(max_n-10, max_n+10, 1):
    rfc = RandomForestClassifier(n_estimators=i+1, random_state=random_state)
    score = rfc.fit(X_train, y_train).score(X_va, y_va)
    score_lt.append(score)

score_max = max(score_lt)
print(score_lt)
final_n_estimators = max_n-10+score_lt.index(score_max)+1
print('最大得分：{}'.format(score_max),
      '子树数量为：{}'.format(final_n_estimators))

# 根据找到的n_estimators 进行拟合，看值

rfc = RandomForestClassifier(n_estimators=final_n_estimators, random_state=random_state)
score = rfc.fit(X_train, y_train).score(X_test, y_test)
print(score)

# 调第二个参数 max_depth
# 建立n_estimators为45的随机森林
rfc = RandomForestClassifier(n_estimators=final_n_estimators, random_state=random_state)

# 用网格搜索调整max_depth
param_grid = {'max_depth': np.arange(1, 20)}
GS = GridSearchCV(rfc, param_grid, cv=10)
GS.fit(X_train, y_train)

best_param = GS.best_params_
print(best_param)


rfc = RandomForestClassifier(n_estimators=final_n_estimators, random_state=random_state, max_depth=3)
score = rfc.fit(X_train, y_train).score(X_test, y_test)
print(score)

# 用网格搜索调整min_samples_leaf
param_grid = {'min_samples_leaf': np.arange(1, 20)}
GS = GridSearchCV(rfc, param_grid, cv=10)
GS.fit(X_train, y_train)

best_param = GS.best_params_
print(best_param)
# 发现就是默认值 1




# team_2020_ada = AdaBoostClassifier(random_state=random_state, n_estimators=10)
# team_2020_bag = BaggingClassifier(random_state=random_state, n_estimators=10)
# # team_2020_xgb = XGBClassifier(random_state=random_state, n_estimators=10)
#
# # rf
# team_2020_rf = team_2020_rf.fit(X_train, y_train)
# print('Train score:{:.3f}'.format(team_2020_rf.score(X_train, y_train)))
# print('Test score:{:.3f}'.format(team_2020_rf.score(X_test, y_test)))
#
# # ada
# team_2020_ada = team_2020_ada.fit(X_train, y_train)
# print('Train score:{:.3f}'.format(team_2020_ada.score(X_train, y_train)))
# print('Test score:{:.3f}'.format(team_2020_ada.score(X_test, y_test)))
#
# # bag
# team_2020_bag = team_2020_bag.fit(X_train, y_train)
# print('Train score:{:.3f}'.format(team_2020_bag.score(X_train, y_train)))
# print('Test score:{:.3f}'.format(team_2020_bag.score(X_test, y_test)))
#
# # # xgb
# # team_2020_xgb = team_2020_xgb.fit(X_train, y_train)
# # print('Train score:{:.3f}'.format(team_2020_xgb.score(X_train, y_train)))
# # print('Test score:{:.3f}'.format(team_2020_xgb.score(X_test, y_test)))