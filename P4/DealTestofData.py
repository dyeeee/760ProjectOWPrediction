import numpy as np
import random
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

# 创建游标
cur = conn.cursor()

# 查询match_result_2020表的所需字段数据
cur.execute("select * from team_match_stat_all_2020to2021")
result = cur.fetchall()

# 原始数据 转DF格式
df_result = pd.DataFrame(list(result))





cnum = 76
# 原始数据大小
print("Raw data size：", df_result.shape)
print("Raw data preview \n", df_result.iloc[:, [num for num in range(4, cnum)]])

flist = [num for num in range(4, cnum)]

# 遍历所有team1 找比赛id小于它的 名字等于它的比赛
# 如果比赛数大于5，那么就取 id最大的五场，否则就选择全部  如果没有比赛，先都设为0吧

p = df_result.copy(deep=True)
t1_index = [num for num in range(4, cnum, 2)]
t2_index = [num for num in range(5, cnum, 2)]

n_size = 3

for i in range(1, df_result.shape[0]):
    print(i)

    q = df_result[(df_result.iloc[:, 0] < df_result.iloc[i, 0])]  # 所有这场比赛之前的场次

    qq1 = q[(q.iloc[:, 1] == df_result.iloc[i, 1]) | (q.iloc[:, 2] == df_result.iloc[i, 1])]  # 包含队伍1的之前的场次
    qq2 = q[(q.iloc[:, 1] == df_result.iloc[i, 2]) | (q.iloc[:, 2] == df_result.iloc[i, 2])]  # 包含队伍2的之前的场次

    print("qq1", qq1)

    if qq1.shape[0] == 0:
        # print("t1的数据全是0")
        p.iloc[i, t1_index] = [0 for _ in range(4, cnum, 2)]
    elif qq1.shape[0] < n_size:
        # print("判断主场还是客场，分别取全部的数据")
        t1_rseult = np.array([0 for _ in range(4, cnum, 2)])
        qq1_index = 0
        for index, row in qq1.iterrows():
            print("qq1index", qq1_index)
            if row[1] == df_result.iloc[i, 1]:
                t1_rseult = t1_rseult + np.array(qq1.iloc[qq1_index, t1_index])
            else:
                t1_rseult = t1_rseult + np.array(qq1.iloc[qq1_index, t2_index])
            qq1_index += 1
        t1_rseult = t1_rseult / qq1.shape[0]
        p.iloc[i, t1_index] = t1_rseult.tolist()
    else:
        # print("判断主场还是客场，取5场")
        qq1 = qq1.sort_values(by=0, axis=0, ascending=False)
        qq1 = qq1.iloc[0:n_size]
        t1_rseult = np.array([0 for _ in range(4, cnum, 2)])
        qq1_index = 0
        for index, row in qq1.iterrows():
            if row[1] == df_result.iloc[i, 1]:
                t1_rseult = t1_rseult + np.array(qq1.iloc[qq1_index, t1_index])
            else:
                t1_rseult = t1_rseult + np.array(qq1.iloc[qq1_index, t2_index])
            qq1_index += 1
        t1_rseult = t1_rseult / 5
        p.iloc[i, t1_index] = t1_rseult.tolist()

    if qq2.shape[0] == 0:
        # print("t1的数据全是0")
        p.iloc[i, t2_index] = [0 for _ in range(4, cnum, 2)]
    elif qq2.shape[0] < n_size:
        # print("判断主场还是客场，分别取全部的数据")
        t2_rseult = np.array([0 for _ in range(4, cnum, 2)])
        qq2_index = 0
        for index, row in qq2.iterrows():
            if row[1] == df_result.iloc[i, 2]:
                t2_rseult = t2_rseult + np.array(qq2.iloc[qq2_index, t1_index])
            else:
                print("qq2index", qq2_index)
                t2_rseult = t2_rseult + np.array(qq2.iloc[qq2_index, t2_index])
            qq2_index += 1
        t2_rseult = t2_rseult / qq1.shape[0]
        p.iloc[i, t2_index] = t2_rseult.tolist()
    else:
        # print("判断主场还是客场，取5场")
        qq2 = qq2.sort_values(by=0, axis=0, ascending=False)
        qq2 = qq2.iloc[0:n_size]
        t2_rseult = np.array([0 for _ in range(4, cnum, 2)])
        qq2_index = 0
        for index, row in qq2.iterrows():
            if row[1] == df_result.iloc[i, 2]:
                t2_rseult = t2_rseult + np.array(qq2.iloc[qq2_index, t1_index])
            else:
                t2_rseult = t2_rseult + np.array(qq2.iloc[qq2_index, t2_index])
            qq2_index += 1
        t2_rseult = t2_rseult / n_size
        p.iloc[i, t2_index] = t2_rseult.tolist()

    # q = df_result[(df_result.iloc[:, 1] == df_result.iloc[i, 1]) & (df_result.iloc[:, 0] < df_result.iloc[i, 0])]
    # if q.shape[0] == 0:
    #     p.iloc[i, flist] = [0 for _ in range(4, cnum)]
    #     print(p.iloc[i, 1], "之前没有比赛")
    # elif q.shape[0] < 5:
    #     # 小于5场，设置为他们所有的和的均值
    #     q = q.sort_values(by=0, axis=0, ascending=False)
    #     # print(q, i, q.shape[0])
    #     p.iloc[i, flist] = q.iloc[0:q.shape[0], flist].mean()
    #     # print(q.iloc[0:q.shape[0], [3, 4, 5, 6]].mean().T)
    # else:
    #     # 选取前五场
    #     q = q.sort_values(by=0, axis=0, ascending=False)
    #
    #     p.iloc[i, flist].update(q.iloc[0:5, flist].mean())

pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# print(p.iloc[:, [0, 2, 3, 4, 5, 6]])

# 一句话
# x = df_result[(df_result.iloc[:,2] == "Vancouver Titans") & (df_result.iloc[:,0].astype(int) < 34811)]
# x = x.sort_values(by=0, axis=0,  ascending=False)
# print(x.iloc[:,[3, 4]])
# o  = x.iloc[0:5, [3, 4, 5, 6]].mean()
# print(pd.DataFrame(o).T)
cur.close()


# 找列名
cur1 = conn.cursor()
cur1.execute("SELECT COLUMN_NAME  FROM information_schema.columns WHERE table_name='team_match_stat_all_2020to2021'")
result1 = cur1.fetchall()

columnName = list(result1)
i = 0
for x in columnName:
    columnName[i] = x[0]
    i = i+1

# 将列名给df
p.columns = columnName
