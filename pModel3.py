# import xgboost as xgb
# from xgboost import plot_importance
from matplotlib import pyplot as plt
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

data = df.iloc[:, pr_index]
response = df["t1_win"]

test_Data = test_df.iloc[:, pr_index]
test_response = test_df["t1_win"]

X_train, y_train = data, response
X_test, y_test = test_Data, test_response

# lf = SVC(C=1.0, cache_size=200, coef0=0.0, degree=3,
#          gamma='auto', kernel='rbf', max_iter=-1, shrinking=True,
#          tol=0.001, verbose=False)

lf = SVC(kernel='rbf', random_state=100, max_iter=-1, cache_size=200, C=1)
clf = lf.fit(X_train, y_train)
print('Train score:{:.10f}'.format(clf.score(X_train, y_train)))
print('Test score:{:.8f}'.format(clf.score(X_test, y_test)))

# score_lt = []
# for i in range(1, 1000):
#     lf = SVC(kernel='rbf', random_state=100, max_iter=-1, cache_size=200, C=i)
#     score = cross_val_score(lf, X_train, y_train, cv=5).mean()
#     score_lt.append(score)
# score_max = max(score_lt)
# print('最大得分：{}'.format(score_max),
#       '子树数量为：{}'.format(score_lt.index(score_max)+1))
#
# # 绘制学习曲线
# x = np.arange(1, 1000)
# plt.subplot(111)
# plt.plot(x, score_lt,'o-')
# plt.show()





# # 开调
# tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
#                      'C': [1, 10, 100]},
#                     {'kernel': ['linear'], 'C': [1, 10, 100]}]
#
#
#
# # 调用 GridSearchCV，将 SVC(), tuned_parameters, cv=5, 还有 scoring 传递进去，
# clf = GridSearchCV(SVC(), tuned_parameters, cv=5,
#                    scoring='precision_macro')
# # 用训练集训练这个学习器 clf
# print("111")
# clf.fit(X_train, y_train)
#
# print("Best parameters set found on development set:")
# print()
#
# # 再调用 clf.best_params_ 就能直接得到最好的参数搭配结果
# print(clf.best_params_)
