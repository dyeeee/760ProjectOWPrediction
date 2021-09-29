import xgboost as xgb
from xgboost import plot_importance
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import warnings
from xgboost.sklearn import XGBClassifier
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.model_selection import GridSearchCV

from sklearn.svm import SVC

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
new_index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14, 41]

data = df.iloc[:, [41]]
response = df["t1_win"]

test_Data = test_df.iloc[:, [41]]
test_response = test_df["t1_win"]

X_train, y_train = data, response
X_test, y_test = test_Data, test_response

# rf
#
# param_lst2 = {
#     "max_depth": [1, 2, 3, 4, 5, 10],
#     "n_estimators": [10, 50, 100]
# }
#
# model = RandomForestClassifier()
# grid_search = GridSearchCV(model, param_grid=param_lst2, cv=10,
#                            verbose=10, n_jobs=-1)
#
# # 基于flights数据集执行搜索
# grid_search.fit(X_train, y_train)
# # 输出搜索结果
# print(grid_search.best_estimator_)


clf = SVC(kernel='rbf', probability=True)
clf = clf.fit(X_train, y_train)
print('Train score:{:.3f}'.format(clf.score(X_train, y_train)))
print('Test score:{:.3f}'.format(clf.score(X_test, y_test)))

print()

lf = SVC(C=1.0, cache_size=200, coef0=0.0, degree=3,
         gamma='auto_deprecated', kernel='rbf', max_iter=-1, shrinking=True,
         tol=0.001, verbose=False)
clf = clf.fit(X_train, y_train)
print('Train score:{:.3f}'.format(clf.score(X_train, y_train)))
print('Test score:{:.3f}'.format(clf.score(X_test, y_test)))
