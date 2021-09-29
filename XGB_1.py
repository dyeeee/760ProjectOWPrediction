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

seed = 7
np.random.seed(seed)

df = pd.read_table("./P3_Data/OWL_Data_team_match_stat_all_2020_withRank_v3.csv", sep=",")
test_df = pd.read_table("./P3_Data/OWL_Data_TESTSET_V3.csv", sep=",")

# split data & response
# data = df.iloc[:, 4:]
# response = df["t1_win"]
#
# test_Data = test_df.iloc[:, 5:]
# test_response = test_df["3"]
new_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14]
off_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14, 40]
pag_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14, 41]
pr_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14, 42]
add_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14, 41, 42]

data = df.iloc[:, off_index]
response = df["t1_win"]

test_Data = test_df.iloc[:, off_index]
test_response = test_df["t1_win"]

X_train, y_train = data, response
X_test, y_test = test_Data, test_response
X_test.columns = X_train.columns

# X_va, y_va = test_Data.iloc[0:100], test_response.iloc[0:100]
# X_test, y_test = test_Data.iloc[101:282], test_response.iloc[101:282]

# 性能评估以XGboost为例
xgb = xgb.XGBClassifier()
# 对训练集训练模型
xgb.fit(X_train, y_train)
# 对测试集进行预测
y_pred = xgb.predict(X_test)
print("\n模型的平均准确率（mean accuracy = (TP+TN)/(P+N) ）")
print("\tXgboost：", xgb.score(X_test, y_test))
# print('(y_test,y_pred)', y_test,y_pred)    print("\n性能评价：")
print("\t预测结果评价报表：\n", metrics.classification_report(y_test, y_pred))
print("\t混淆矩阵：\n", metrics.confusion_matrix(y_test, y_pred))

from sklearn.model_selection import GridSearchCV

# from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
#
# # 创建xgb分类模型实例
# model = XGBClassifier()
# # 待搜索的参数列表空间
# param_lst = {
#     'n_estimators': range(80, 200, 4),
#     'max_depth': range(2, 15, 1),
#     'learning_rate': np.linspace(0.01, 2, 20),
#     'subsample': np.linspace(0.7, 0.9, 20),
#     'colsample_bytree': np.linspace(0.5, 0.98, 10),
#     'min_child_weight': range(1, 9, 1)
# }
#
# param_lst2 = {
#     "max_depth": [3, 5, 7, 10],
#     "n_estimators": [100, 200, 300],
#     "learning_rate": [0.001, 0.05, 0.1]
# }
#
# # 创建网格搜索
# grid_search = GridSearchCV(model, param_grid=param_lst2, cv=10,
#                            verbose=10, n_jobs=-1)
#
# # 基于flights数据集执行搜索
# grid_search.fit(X_train, y_train)
# # 输出搜索结果
# print(grid_search.best_estimator_)

# xgb2 = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
#                      colsample_bynode=1, colsample_bytree=1, gamma=0, gpu_id=-1,
#                      importance_type='gain', interaction_constraints='',
#                      learning_rate=0.05, max_delta_step=0, max_depth=5,
#                      min_child_weight=1, monotone_constraints='()',
#                      n_estimators=100, n_jobs=0, num_parallel_tree=1, random_state=0,
#                      reg_alpha=0, reg_lambda=1, scale_pos_weight=1, subsample=1,
#                      tree_method='exact', validate_parameters=1, verbosity=None)
#
# # 对训练集训练模型
# xgb2.fit(X_train, y_train)
# # 对测试集进行预测
# y_pred = xgb2.predict(X_test)
# print("\n模型的平均准确率（mean accuracy = (TP+TN)/(P+N) ）")
# print("\tXgboost：", xgb2.score(X_test, y_test))
# # print('(y_test,y_pred)', y_test,y_pred)    print("\n性能评价：")
# print("\t预测结果评价报表：\n", metrics.classification_report(y_test, y_pred))
# print("\t混淆矩阵：\n", metrics.confusion_matrix(y_test, y_pred))


score_lt = []

for i in range(0, 200, 10):
    rfc = XGBClassifier(n_estimators=i + 1
                        , random_state=90)
    score = cross_val_score(rfc, X_train, y_train, cv=10).mean()
    score_lt.append(score)
score_max = max(score_lt)
print('最大得分：{}'.format(score_max),
      '子树数量为：{}'.format(score_lt.index(score_max) * 10 + 1))

# 绘制学习曲线
x = np.arange(1, 201, 10)
plt.subplot(111)
plt.plot(x, score_lt, 'r-')
plt.xlabel('n_estimators')
plt.ylabel('accuracy')
plt.show()

score_lt = []
for i in range(40, 60):
    rfc = XGBClassifier(n_estimators=i + 1
                        , random_state=90)
    score = cross_val_score(rfc, X_train, y_train, cv=10).mean()
    score_lt.append(score)
score_max = max(score_lt)
print('最大得分：{}'.format(score_max),
      '子树数量为：{}'.format(score_lt.index(score_max) + 1))

# 绘制学习曲线
x = np.arange(11, 31)
plt.subplot(111)
plt.plot(x, score_lt, 'r-')
plt.xlabel('n_estimators')
plt.ylabel('accuracy')
plt.show()

xgb = XGBClassifier(random_state=999, n_estimators=10)
print(cross_val_score(xgb, X_test, y_test, cv=10).mean())

score_lt = []
for i in range(0, 20):
    rfc = XGBClassifier(n_estimators=10
                        , random_state=90)
    score = cross_val_score(rfc, X_train, y_train, cv=10).mean()
    score_lt.append(score)
score_max = max(score_lt)
print('最大得分：{}'.format(score_max),
      '子树数量为：{}'.format(score_lt.index(score_max) + 1))

# 绘制学习曲线
x = np.arange(1, 21)
plt.subplot(111)
plt.plot(x, score_lt, 'r-')
plt.xlabel('n_estimators')
plt.ylabel('accuracy')
plt.show()
