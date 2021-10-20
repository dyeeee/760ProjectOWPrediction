import lightgbm as lgb
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from sklearn.preprocessing import label_binarize
from sklearn.metrics import *
from sklearn.model_selection import train_test_split, cross_val_score
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
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

X_train_1, y_train_1 = train_df.iloc[0:296, off_list], response.iloc[0:296]
X_train_2, y_train_2 = train_df.iloc[0:296, team_rank], response.iloc[0:296]
X_train_3, y_train_3 = train_df.iloc[0:296, player_list], response.iloc[0:296]
X_train_4, y_train_4 = train_df.iloc[0:296, off_list + team_rank], response.iloc[0:296]
X_train_5, y_train_5 = train_df.iloc[0:296, off_list + player_list], response.iloc[0:296]
X_train_6, y_train_6 = train_df.iloc[0:296, team_rank + player_list], response.iloc[0:296]
X_train_7, y_train_7 = train_df.iloc[0:296, off_list + team_rank + player_list], response.iloc[0:296]

X_list = [X_train_1, X_train_2, X_train_3, X_train_4, X_train_5, X_train_6, X_train_7]
y_list = [y_train_1, y_train_2, y_train_3, y_train_4, y_train_5, y_train_6, y_train_7]

X_test, y_test = train_df.iloc[296:, team_rank + player_list], response.iloc[296:]

# 训练

train_data = lgb.Dataset(X_train_6, label=y_train_6)
validation_data = lgb.Dataset(X_test, label=y_test)

# 将参数写成字典下形式
params = {
    'task': 'train',
    'boosting_type': 'gbdt',  # 设置提升类型
    'objective': 'regression',  # 目标函数
    'metric': {'l2', 'auc'},  # 评估函数
    'num_leaves': 31,  # 叶子节点数
    'learning_rate': 0.05,  # 学习速率
    'feature_fraction': 0.9,  # 建树的特征选择比例
    'bagging_fraction': 0.8,  # 建树的样本采样比例
    'bagging_freq': 5,  # k 意味着每 k 次迭代执行bagging
    'verbose': 1  # <0 显示致命的, =0 显示错误 (警告), >0 显示信息
}

print('Start training...')
# 训练 cv and train
gbm = lgb.train(params, train_data, num_boost_round=20, valid_sets=validation_data,
                early_stopping_rounds=5)  # 训练数据需要参数列表和数据集

print('Save model...')

gbm.save_model('model.txt')  # 训练后保存模型到文件

print('Start predicting...')
# 预测数据集
y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)  # 如果在训练期间启用了早期停止，可以通过best_iteration方式从最佳迭代中获得预测
# 评估模型
print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)  # 计算真实值和预测值之间的均方根误差

threshold = 0.5
result = []
for pred in y_pred:
    if pred > threshold:
        result.append(1)
    else:
        result.append(0)

print(classification_report(y_test, result, digits=4))

for i in [0.6, 0.65, 0.67, 0.66]:
    result = []
    for pred in y_pred:
        if pred > i:
            result.append(1)
        else:
            result.append(0)

    print(classification_report(y_test, result, digits=4))
