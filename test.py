from sklearn.preprocessing import Normalizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest, f_regression
from scipy.stats import pearsonr
from array import array
import numpy as np
import pandas as pd
import pymysql
from sklearn.feature_selection import SelectKBest
from minepy import MINE
from sklearn.feature_selection import RFE
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression,Ridge,Lasso

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
cur.execute("select * from all_heroes_stat_all_2020_FeatureSelection")
result = cur.fetchall()

# 原始数据 转DF格式
df_result = pd.DataFrame(list(result))

# 找列名
cur1 = conn.cursor()
cur1.execute("SELECT COLUMN_NAME  FROM information_schema.columns WHERE table_name='all_heroes_stat_all_2020_FeatureSelection'")
result1 = cur1.fetchall()

columnName = list(result1)
i = 0
for x in columnName:
    columnName[i] = x[0]
    i = i+1

# 将列名给df
df_result.columns = columnName

print(df_result.head())

print(df_result.loc[:, ['esports_match_id', 'map_name', 'team_name', 'Eliminations']])

df_x = df_result.drop(columns=['esports_match_id', 'map_name', 'team_name', 'Eliminations'])
df_y = df_result.loc[:, ['Eliminations']].values

df_data = df_x.values
df_target = df_y.ravel()


# 方差选择法，返回值为特征选择后的数据
# 参数threshold为方差的阈值
# q = VarianceThreshold(threshold=3).fit_transform(df_x)
# print(q)

# 选择K个最好的特征，返回选择特征后的数据
# 第一个参数为计算评估特征是否好的函数，该函数输入特征矩阵和目标向量，输出二元组（评分，P值）的数组，数组第i项为第i个特征的评分和P值。在此定义为计算相关系数
# 参数k为选择的特征个数              data为特征矩阵  target为目标向量
p = SelectKBest(f_regression, k=15).fit(df_data, df_target).get_support(indices=True)
print(p)

print(df_x.iloc[:, p].columns)


# 递归特征消除法，返回特征选择后的数据：
# 参数estimator为基模型
# 参数n_features_to_select为选择的特征个数
# lr = Ridge(alpha=100000, fit_intercept=True, normalize=True,
#            copy_X=True, max_iter=1500, tol=1e-4, solver='auto')
# p2 = RFE(estimator=lr, n_features_to_select=15).fit(df_data, df_target).get_support(indices=True)
# print(p2)
# print(df_x.iloc[:, p2].columns)
