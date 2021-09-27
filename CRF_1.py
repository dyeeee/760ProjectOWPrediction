import pandas as pd
import string
import pycrfsuite
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
from collections import Counter



df = pd.read_table("./Subdata/team_match_stat_2020.csv", sep=",")
test_df = pd.read_table("./Subdata/TEST_team_match_stat_2020.csv", sep=",")

# split data & response
data = df.iloc[:, 2:]
response = df["t1_win"]

test_Data = test_df.iloc[:, 2:]
test_response = test_df["t1_win"]

X_train, y_train = data, response
X_test, y_test = test_Data, test_response

crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(X_train, y_train)

y_pred = crf.predict(X_test)
print(metrics.flat_classification_report(y_test, y_pred))