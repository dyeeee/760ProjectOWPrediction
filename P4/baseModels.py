import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold, StratifiedKFold, RepeatedKFold
from autorank import autorank, create_report, plot_stats
from xgboost import XGBClassifier


df = pd.read_table("../P_Data/OWL_Data_team_match_stat_all_2020to2021.csv", sep=",")
test_df = pd.read_table("../P_Data/TESTSET_V4.csv", sep=",")

# split data & response
data = df.iloc[:, 2:]
response = df["t1_win"]

test_Data = test_df.iloc[:, 5:]
test_response = test_df["t1_win"]

X_train, y_train = data, response
X_test, y_test = test_Data, test_response


# 4. Modeling by repeated-cross-validation
model_names = ["RF", "Ada", "Bagging", "XGB"]
model_names_index = 0
scores_df = pd.DataFrame()

# random_state
random_state = 999
# models
rf = RandomForestClassifier(random_state=random_state, n_estimators=10)
ada = AdaBoostClassifier(random_state=random_state, n_estimators=10)
bag = BaggingClassifier(random_state=random_state, n_estimators=10)
xgb = XGBClassifier(random_state=random_state, n_estimators=10)

# rf
rf = rf.fit(X_train, y_train)
print('Train score:{:.3f}'.format(rf.score(X_train, y_train)))
print('Test score:{:.3f}'.format(rf.score(X_test, y_test)))

# ada
ada = ada.fit(X_train, y_train)
print('Train score:{:.3f}'.format(ada.score(X_train, y_train)))
print('Test score:{:.3f}'.format(ada.score(X_test, y_test)))

# bag
bag = bag.fit(X_train, y_train)
print('Train score:{:.3f}'.format(bag.score(X_train, y_train)))
print('Test score:{:.3f}'.format(bag.score(X_test, y_test)))

# xgb
xgb = xgb.fit(X_train, y_train)
print('Train score:{:.3f}'.format(xgb.score(X_train, y_train)))
print('Test score:{:.3f}'.format(xgb.score(X_test, y_test)))