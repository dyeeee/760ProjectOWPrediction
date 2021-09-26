from sklearn.preprocessing import Normalizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
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

cur


print(df_result.head())
