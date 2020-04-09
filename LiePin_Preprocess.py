

'''
猎聘网-数据预处理
'''

import numpy as np
import pandas as pd
import re


pd.set_option('display.max_columns', None) #显示所有列
pd.set_option('display.max_rows', None) #显示所有行


## 读取数据

file_name = r'data\data_ana\liepin_jobs_数据分析_010_10.csv'
df = pd.read_csv(file_name,index_col=0)


### 删除重复值

lst = df.columns.to_list()
lst.remove('发布时间')
df = df.drop_duplicates(subset = lst,inplace = False)
df = df.reset_index(drop=True)


## 某些字段列表转字符串

df.薪资 = ["".join(eval(item)) for item in df.薪资]
df.公司位置 = ["".join(eval(item)) for item in df.公司位置]
df.学历 = ["".join(eval(item)) for item in df.学历]
df.工作年限 = ["".join(eval(item)) for item in df.工作年限]


## 发布时间转成时间类型

s = df.发布时间
sn = [pd.to_datetime(re.sub('[年月日]','-',item)) for item in s]
df.发布时间 = sn


## 从工资字段提取最低、最高工资和一年发多少月的工资

df.薪资[df.薪资 == '面议'] = '0-0·0薪'

s = df.薪资
s1,s2,s3 = zip(*[re.split('-|·',re.sub('[kK薪]','',item)) \
               for item in s])

s1 = [int(i) for i in s1]
s2 = [int(i) for i in s2]
s3 = [int(i) for i in s3]

df.drop(['薪资'],axis=1,inplace=True)
df['最低工资'] = s1
df['最高工资'] = s2
df['薪资月数'] = s3


## 工作年限转为数字

df.工作年限.unique()

s = df.工作年限
s = s.replace({'3年以上':'3', '5年以上':'5', '1年以上':'1', \
               '经验不限':'0', '8年以上':'8', '2年以上':'2', \
               '6年以上':'6', '4年以上':'4','7年以上':'7', \
               '10年以上':'10'})

s = [eval(item) for item in s]
df.工作年限 = s


## 学历分类整理

df.学历.unique()

s = df.学历
s = s.replace({'统招本科':'本科', '本科及以上':'本科', \
               '大专及以上':'大专', '硕士及以上':'硕士', '学历不限':'不限'})

df.学历 = s


## 公司人数处理

s = df.公司人数
lst = s.to_list()
se = ["['10000']", "['1', '49']", "['100', '499']","['5000', '10000']", \
      "['500', '999']", "['50', '99']","['2000', '5000']", "['1000', '2000']"]
ss = list(map(lambda x:x if x in se else "['0']",lst))

df.公司人数 = [eval(item) for item in ss]


## 数据筛选

df = df.loc \
        [:,('公司名','公司领域','公司人数',\
            '学历','最低工资','最高工资',\
            '工作年限','岗位职责','岗位要求')]


## 保存预处理的数据

df.to_csv(file_name.replace('.','_new.'))
