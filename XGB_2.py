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
X_test.columns = X_train.columns

# for i in range(30, 50):
xgb = XGBClassifier(random_state=999, n_estimators=30, max_depth=2, learning_rate=0.1)
print(cross_val_score(xgb, X_train, y_train, cv=10).mean())
