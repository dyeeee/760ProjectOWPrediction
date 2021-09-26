import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold, StratifiedKFold, RepeatedKFold
from autorank import autorank, create_report, plot_stats
from xgboost import XGBClassifier

df = pd.read_table("./Subdata/team_match_stat_2020.csv", sep=",")
test_df = pd.read_table("./Subdata/TEST_team_match_stat_2020.csv", sep=",")

# split data & response
data = df.iloc[:, 2:]
response = df["t1_win"]

test_Data = test_df.iloc[:, 2:]
test_response = test_df["t1_win"]

X_train, y_train = data, response
X_test, y_test = test_Data, test_response

# 4. Modeling by repeated-cross-validation
model_names = ["RF", "Ada", "Bagging", "XGB"]
model_names_index = 0
team_2020_scores_df = pd.DataFrame()

# random_state
random_state = 999
# models
team_2020_rf = RandomForestClassifier(random_state=random_state, n_estimators=10)
team_2020_ada = AdaBoostClassifier(random_state=random_state, n_estimators=10)
team_2020_bag = BaggingClassifier(random_state=random_state, n_estimators=10)
team_2020_xgb = XGBClassifier(random_state=random_state, n_estimators=10)

# rf
team_2020_rf = team_2020_rf.fit(X_train, y_train)
print('Train score:{:.3f}'.format(team_2020_rf.score(X_train, y_train)))
print('Test score:{:.3f}'.format(team_2020_rf.score(X_test, y_test)))

# ada
team_2020_ada = team_2020_ada.fit(X_train, y_train)
print('Train score:{:.3f}'.format(team_2020_ada.score(X_train, y_train)))
print('Test score:{:.3f}'.format(team_2020_ada.score(X_test, y_test)))

# bag
team_2020_bag = team_2020_bag.fit(X_train, y_train)
print('Train score:{:.3f}'.format(team_2020_bag.score(X_train, y_train)))
print('Test score:{:.3f}'.format(team_2020_bag.score(X_test, y_test)))

# xgb
team_2020_xgb = team_2020_xgb.fit(X_train, y_train)
print('Train score:{:.3f}'.format(team_2020_xgb.score(X_train, y_train)))
print('Test score:{:.3f}'.format(team_2020_xgb.score(X_test, y_test)))