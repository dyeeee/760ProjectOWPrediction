from catboost import CatBoostClassifier
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np

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

model = CatBoostClassifier(iterations=20, depth=5, learning_rate=0.5, loss_function='Logloss',
                           logging_level='Verbose')

model.fit(X_train_6, y_train_6)
# Get predicted classes
preds_class = model.predict(X_test)
# Get predicted probabilities for each class
preds_proba = model.predict_proba(X_test)

score2 = cross_val_score(model, X_train_6, y_train_6, cv=10)
print("训练精度: ", score2.mean())
d = np.std(score2)
print("标准差: ", d)

score = model.score(X_test, y_test)
print("测试精度: ", score)
