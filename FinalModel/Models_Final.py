from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from sklearn.preprocessing import label_binarize
from sklearn.metrics import *
from sklearn.model_selection import train_test_split, cross_val_score
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

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

X_train_1, y_train_1 = train_df.iloc[0:296, off_list], response.iloc[0:296]
X_train_2, y_train_2 = train_df.iloc[0:296, team_rank], response.iloc[0:296]
X_train_3, y_train_3 = train_df.iloc[0:296, player_list], response.iloc[0:296]
X_train_4, y_train_4 = train_df.iloc[0:296, off_list + team_rank], response.iloc[0:296]
X_train_5, y_train_5 = train_df.iloc[0:296, off_list + player_list], response.iloc[0:296]
X_train_6, y_train_6 = train_df.iloc[0:296, team_rank + player_list], response.iloc[0:296]
X_train_7, y_train_7 = train_df.iloc[0:296, off_list + team_rank + player_list], response.iloc[0:296]

X_list = [X_train_1, X_train_2, X_train_3, X_train_4, X_train_5, X_train_6, X_train_7]
y_list = [y_train_1, y_train_2, y_train_3, y_train_4, y_train_5, y_train_6, y_train_7]

X_test, y_test = train_df.iloc[296:, team_rank+player_list], response.iloc[296:]

scaler = StandardScaler()
std_Xtrain = scaler.fit_transform(X_train_6)

scaler = StandardScaler()
std_Xtest = scaler.fit_transform(X_test)

lr_clf = LogisticRegression(
    random_state=random_state, penalty='l2', C=1.0)

lr_clf.fit(std_Xtrain, y_train_2)
score2 = cross_val_score(lr_clf, std_Xtrain, y_train_2, cv=10)

# 调参数
# 1、AUC
# y_pred_pa = lr_clf.predict_proba(X_test)
# y_test_oh = label_binarize(y_test, classes=[0, 1])
# print('调用函数auc：', roc_auc_score(y_test_oh, y_pred_pa, average='micro'))
predictions = lr_clf.predict_proba(std_Xtest)  # 每一类的概率
false_positive_rate, recall, thresholds = roc_curve(y_test, predictions[:
, 1])
roc_auc = auc(false_positive_rate, recall)
print("AUC：", roc_auc)

plt.title('Receiver Operating Characteristic')
plt.plot(false_positive_rate, recall, 'b', label='AUC = %0.2f' % roc_auc)
plt.legend(loc='lower right')
plt.plot([0, 1], [0, 1], 'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.ylabel('Recall')
plt.xlabel('Fall-out')
plt.show()

#  2、混淆矩阵
y_pred = lr_clf.predict(std_Xtest)


# for t in thresholds:
#     y_pred_new = []
#     print(t)
#     for y in predictions:
#         if y[0] > t:
#             y_pred_new.append(0)
#         else:
#             y_pred_new.append(1)
#     print(classification_report(y_test, y_pred_new, digits=4))

# confusion_matrix(y_test, y_pred)

#  3、经典-精确率、召回率、F1分数

print("训练精度: ", score2.mean())
d = np.std(score2)
print("标准差: ", d)
precision_score(y_test, y_pred, average='micro')
recall_score(y_test, y_pred, average='micro')
f1_score(y_test, y_pred, average='micro')

print("AUC：", roc_auc)

# 4、模型报告
print(classification_report(y_test, y_pred, digits=4))

score = lr_clf.score(std_Xtest, y_test)
print("测试精度: ", score)
