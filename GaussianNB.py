import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
import pymysql
import pandas as pd

# 链接数据库
conn = pymysql.connect(
    host="8.129.120.114",
    port=3306,
    user="root",
    passwd="123",
    db="OWL_Data"
)

# 创建游标
cur = conn.cursor()

# 查询match_result_2020表的所需字段数据
cur.execute("select * from team_match_stat_2020")
result = cur.fetchall()
df_result = pd.DataFrame(list(result),
                         columns=["match_id", "t1_win", "avg_10_t1_Hero_Damage_Done", "avg_10_t1_Final_Blows",
                                  "avg_10_t1_Healing_done", "avg_10_t1_Deaths",
                                  "avg_10_t2_Hero_Damage_done", "avg_10_t2_Final_Blows", "avg_10_t2_Healing_done",
                                  "avg_10_t2_Deaths"])

print(df_result.head())
df_X = df_result.iloc[:, 2:10]
df_Y = df_result.iloc[:, 1]
X = df_X.values.tolist()
Y = df_X.values.tolist()

RepeatedKF = RepeatedKFold(n_splits=10, n_repeats=10, random_state=1000)

# # 特征
# X = np.array([[0, 39, 79, 9, 22, 22, 28, 6, 42, 24, 20, 7, 7, 33, 109], [0, 34, 85, 9, 24, 12, 15, 9, 33, 16, 14, 4, 3,
# 23, 89], [0, 38, 88, 2, 19, 20, 25, 4, 32, 21, 4, 7, 4, 22, 98], [1, 32, 81, 6, 19, 16, 21, 5, 33, 16, 9, 3, 8, 3, 86],
# [1, 36, 84, 8, 20, 12, 13, 9, 33, 23, 8, 5, 6, 20, 92], [0, 45, 90, 8, 23, 13, 18, 11, 28, 22, 9, 3, 2, 23, 111]])
# # label
# Y = np.array([1, 0, 0, 0, 0, 0])
# # test case
# y1 = np.array([[1, 52, 76, 4, 25, 15, 13, 6, 36, 22, 12, 3, 6, 35, 111]])
#
# # 朴素贝叶斯
# clf = GaussianNB()
# clf.fit(X, Y)
# print(clf.predict(y1))
#
# # KNN
# Knn = KNeighborsClassifier(n_neighbors=3)
# Knn.fit(X, Y)
# print(Knn.predict(y1))
#
# # SVM
# clf2 = svm.SVC(kernel = 'linear')
#
# clf2.fit(X, Y)
# clf2.predict(y1)
