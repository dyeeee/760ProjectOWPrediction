from sklearn.preprocessing import Normalizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest, f_regression, chi2
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
cur.execute("select * from all_heroes_stat_all_2020_mapwin")
result = cur.fetchall()

# 原始数据 转DF格式
df_result = pd.DataFrame(list(result))

# 找列名
cur1 = conn.cursor()
cur1.execute("SELECT COLUMN_NAME  FROM information_schema.columns WHERE table_name='all_heroes_stat_all_2020_mapwin'")
result1 = cur1.fetchall()

columnName = list(result1)
i = 0
for x in columnName:
    columnName[i] = x[0]
    i = i+1

# 将列名给df
df_result.columns = columnName

print(df_result.head())
# 遍历df表，如果team_name等于map_winner 那么就让map_winner为1 不然就为0
df_result.loc[df_result['team_name'] != df_result['map_winner'], 'map_winner'] = 0
df_result.loc[df_result['team_name'] == df_result['map_winner'], 'map_winner'] = 1

print(df_result)

print(df_result.loc[:, ['esports_match_id', 'map_name', 'team_name', 'Eliminations', 'match_id']])

df_x = df_result.drop(columns=['esports_match_id', 'map_name', 'team_name', 'm_name', 'map_winner'])
df_y = df_result.loc[:, ['map_winner']].values

df_data = df_x.values
df_target = df_y.ravel().astype('int')
print(df_data)
print(df_target)


# 方差选择法，返回值为特征选择后的数据
# 参数threshold为方差的阈值
q = VarianceThreshold(threshold=3).fit(df_x).get_support(indices=True)
print(q)
df_data = df_x.iloc[:, q].values

# 选择K个最好的特征，返回选择特征后的数据
# 第一个参数为计算评估特征是否好的函数，该函数输入特征矩阵和目标向量，输出二元组（评分，P值）的数组，数组第i项为第i个特征的评分和P值。在此定义为计算相关系数
# 参数k为选择的特征个数              data为特征矩阵  target为目标向量
p = SelectKBest(chi2, k=15).fit(df_data, df_target).get_support(indices=True)
print(p)

print(df_x.iloc[:, p].columns)




# 卡方检验
#选择K个最好的特征，返回选择特征后的数据
# bo = SelectKBest(chi2, k=10).fit(df_data, df_target).get_support(indices=True)
# print(bo)
# print(df_x.iloc[:, bo].columns)

# 递归特征消除法，返回特征选择后的数据：
# 参数estimator为基模型
# 参数n_features_to_select为选择的特征个数
# lr = Ridge(alpha=100000, fit_intercept=True, normalize=True,
#            copy_X=True, max_iter=1500, tol=1e-4, solver='auto')
# p2 = RFE(estimator=lr, n_features_to_select=15).fit(df_data, df_target).get_support(indices=True)
# print(p2)
# print(df_x.iloc[:, p2].columns)


# temp = df_x.iloc[:, p]
# print(temp.head())

# 主成分分析法，返回降维后的数据
# 参数n_components为主成分数目
# m = PCA(n_components=5).fit_transform(temp.values)
# print(m)

