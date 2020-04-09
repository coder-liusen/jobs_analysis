

'''
拉勾网-数据预处理
'''

import numpy as np
import pandas as pd
import re


pd.set_option('display.max_columns', None) #显示所有列
pd.set_option('display.max_rows', None) #显示所有行


## 读取数据
file_name = r'data\data_ana\lagou_jobs_数据挖掘_北京_100.csv'
df = pd.read_csv(file_name,index_col=0)


### 删除重复值

lst = df.columns.to_list()
lst.remove('发布时间')
df = df.drop_duplicates(subset = lst,inplace = False)
df = df.reset_index(drop=True)


## 发布时间转成时间类型

s = df.发布时间
sn = pd.Series([pd.to_datetime(item) for item in s])
df.发布时间 = sn


## 从工资字段提取最低和最高工资

s = df.工资
s1,s2 = zip(*[item.replace("k","").replace("K","").split("-") for item in s])
s1 = [int(i) for i in s1]
s2 = [int(i) for i in s2]

df.drop(['工资'],axis=1,inplace=True)
df['最低工资'] = s1
df['最高工资'] = s2


## 从工作年限字段中提取最低工作年限和最高工作年限

df.工作年限.unique() # 查看工作年限有哪几项

df.drop(df[df.工作年限 == '应届毕业生'].index,inplace=True)
df = df.reset_index(drop=True)

s = df.工作年限
s = s.replace({'1-3年':'(1,3)', '3-5年':'(3,5)', '5-10年':'(5,10)',\
               '不限':'(0,0)', '10年以上':'(10,10)', '1年以下':'(0,1)'})
s1,s2 = zip(*[eval(item) for item in s])

df.工作年限 = s


## 公司人数处理

s = df.公司人数
lst =  [re.sub(r'[\u4e00-\u9fa5]','',item).split('-') for item in s]

df.公司人数 = lst


## 数据筛选

df = df.loc \
        [:,('公司名','公司领域','公司人数',\
            '学历','最低工资','最高工资',\
            '工作年限',\
            '岗位职责','岗位要求')]


## 保存预处理的数据

df.to_csv(file_name.replace('.','_new.'))


