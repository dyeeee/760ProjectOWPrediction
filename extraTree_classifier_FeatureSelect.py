from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
import pymysql
import pandas as pd
import numpy as np

conn = pymysql.connect(
    host="8.129.120.114",
    port=3306,
    user="root",
    passwd="123",
    db="OWL_Data"
)
cur = conn.cursor()
cur.execute("select * from all_heroes_stat_all_2020_mapwin")
des = cur.description

col = []
for i in range(len(des)):
    col.append(des[i][0])

df_all_stat = cur.fetchall()
df_all_stat = pd.DataFrame(list(df_all_stat), columns=col)

# print(df_all_stat)
col_imp = col[3:39]
X = df_all_stat.iloc[:, 3:39]

def function(df):
    if df.iloc[2] == df.iloc[41]:
        return 1
    else:
        return 0


y = df_all_stat.apply(function, axis=1)

# print(X.shape)
# print(y.shape)
# print(y)
#clf = ExtraTreesClassifier()
clf = RandomForestClassifier()
clf = clf.fit(X, y)

s_importance = pd.Series(list(clf.feature_importances_), index=col_imp)
s_importance.sort_values(ascending=False, inplace=True)
print(s_importance)

model = SelectFromModel(clf, prefit=True, max_features=15)
X_new = model.transform(X)

#clf_new = ExtraTreesClassifier()
clf_new = RandomForestClassifier();
clf_new = clf_new.fit(X_new, y)
# y_predict = clf_new.predict(X_new)
result = clf_new.score(X_new, y)
print(result)

cur.close()