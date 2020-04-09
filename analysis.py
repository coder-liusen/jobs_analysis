

'''
拉勾/猎聘网站 数据分析/数据挖掘岗位 数据分析
'''

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
from sklearn.cluster import KMeans


## 加载数据
file_lagou_fenxi = r'data\data_ana\lagou_jobs_数据分析_北京_100_new.csv'
file_lagou_wajue = r'data\data_ana\lagou_jobs_数据挖掘_北京_100_new.csv'
file_liepin_fenxi = r'data\data_ana\liepin_jobs_数据分析_010_10_new.csv'
file_liepin_wajue = r'data\data_ana\liepin_jobs_数据挖掘_010_10_new.csv'

df_lagou_fenxi = pd.read_csv(file_lagou_fenxi,index_col=0)
df_lagou_wajue = pd.read_csv(file_lagou_wajue,index_col=0)
df_liepin_fenxi = pd.read_csv(file_liepin_fenxi,index_col=0)
df_liepin_wajue = pd.read_csv(file_liepin_wajue,index_col=0)


## 数据情况显示

print("数据条数：")
print("拉勾-数据分析：",df_lagou_fenxi.shape[0])
print("拉勾-数据挖掘：",df_lagou_wajue.shape[0])
print("猎聘-数据分析：",df_liepin_fenxi.shape[0])
print("猎聘-数据挖掘：",df_liepin_wajue.shape[0])

print("")

print("分析项：")
print("拉勾：",list(df_lagou_fenxi.columns))
print("猎聘：",list(df_liepin_fenxi.columns))


ana_opt = "describe"

## 单字段分析（以拉勾网站为例）

if(ana_opt == "describe"):

    df_1 = df_lagou_fenxi # 数据分析岗位
    df_2 = df_lagou_wajue[:df_1.shape[0]] # 数据挖掘

    describe_opt = "compsize"

    # 数据分析和数据挖掘-学历分布
    if(describe_opt == "edu"):

        lst_1 = df_1.学历.to_list()
        lst_2 = df_2.学历.to_list()

        edu_lst = ['不限', '大专', '本科', '硕士', '博士']

        dic_1 = {key:lst_1.count(key) for key in edu_lst}
        dic_2 = {key:lst_2.count(key) for key in edu_lst}

        x = np.arange(len(dic_1))
        y_1 = dic_1.values()
        y_2 = dic_2.values()
        edu = list(dic_1.keys())

        plt.figure('', facecolor='lightgray')
         
        a = plt.bar(x-0.2 , y_1 , 0.4 ,  color='dodgerblue' , label="数据分析", align='center')
        b = plt.bar(x+0.2 , y_2 , 0.4 ,  color='orangered' , label="数据挖掘", align='center')

        for i in a + b:
            h = i.get_height()
            plt.text(i.get_x() + i.get_width() / 2, h, '%d' % int(h), ha='center', va='bottom')

        plt.tick_params(labelsize=10)
        plt.xticks(x,edu)
        plt.grid(linestyle=':', axis='y')
        plt.title('学历分布图',fontsize=16)
        plt.xlabel('学历',fontsize=16)
        plt.ylabel('需求（岗位数）',fontsize=16)
        
        plt.legend()
        plt.show()

    # 数据分析和数据挖掘-工资分布
    if(describe_opt == "sal"):

        s_1_avgsal = (df_1.最低工资 + df_1.最高工资)/2
        s_2_avgsal = (df_2.最低工资 + df_2.最高工资)/2

        a = list(s_1_avgsal.unique())
        b = list(s_2_avgsal.unique())

        bins = np.arange(0,80,5)

        plt.figure('', facecolor='lightgray')
        
        plt.hist(s_1_avgsal,bins,color='steelblue',alpha=0.5,label='数据分析')
        plt.hist(s_2_avgsal,bins,color='fuchsia',alpha=0.5,label='数据挖掘')

        plt.grid(linestyle=':', axis='y')
        plt.title('工资分布图',fontsize=16)
        plt.xlabel('月薪(k)',fontsize=16)
        plt.ylabel('需求（岗位数）',fontsize=16)
        plt.legend()
        plt.xlim(0,80)

        plt.show()

    # 数据分析和数据挖掘-工作年限分布
    if(describe_opt == "exp"):

        lst_1 = df_1.工作年限.to_list()
        lst_2 = df_2.工作年限.to_list()

        exp_lst = ['(0,0)', '(0,1)', '(1,3)', '(3,5)', '(5,10)','(10,10)']

        dic_1 = {key:lst_1.count(key) for key in exp_lst}
        dic_2 = {key:lst_2.count(key) for key in exp_lst}

        x = np.arange(len(dic_1))
        y_1 = dic_1.values()
        y_2 = dic_2.values()
        exp = list(dic_1.keys())
        exp = ['不限', '1年以下', '1-3年', '3-5年', '5-10年', '10年以上']

        plt.figure('', facecolor='lightgray')
         
        a = plt.bar(x-0.2 , y_1 , 0.4 ,  color='dodgerblue' , label="数据分析",align='center')
        b = plt.bar(x+0.2 , y_2 , 0.4 ,  color='orangered' , label="数据挖掘",align='center')

        for i in a + b:
            h = i.get_height()
            plt.text(i.get_x() + i.get_width() / 2, h, '%d' % int(h), ha='center', va='bottom')

        plt.tick_params(labelsize=10)
        plt.xticks(x,exp)

        plt.grid(linestyle=':', axis='y')
        plt.title('工作年限分布图',fontsize=16)
        plt.xlabel('工作年限',fontsize=16)
        plt.ylabel('需求（岗位数）',fontsize=16)
        plt.legend()
        plt.show()
        
    # 数据分析和数据挖掘-岗位职责和岗位要求分析
    if(describe_opt == "detail"):

        df_1 = df_1.loc[:,('岗位职责','岗位要求')].dropna(how = "any")
        df_2 = df_2.loc[:,('岗位职责','岗位要求')].dropna(how = "any")

        # 岗位职责
        lu_1 = list(df_1.岗位职责.unique())
        lu_2 = list(df_2.岗位职责.unique())

        rpl = re.compile(r'、|\n|,|，|；|。|[1-9]')
        lu_1 = [rpl.sub("",item) for item in lu_1]
        lu_2 = [rpl.sub("",item) for item in lu_2]

        lu_1 = [",".join(jieba.cut(item)) for item in lu_1]
        lu_2 = [",".join(jieba.cut(item)) for item in lu_2]
        

        font = "font\\simhei.ttf"
        
        text = "".join(lu_1)
        wc = WordCloud(font_path = font).generate(text)
        plt.figure('1')
        plt.imshow(wc , interpolation='bilinear')
        plt.title('数据分析-岗位职责词云')
        plt.axis("off")
        plt.show()

        text = "".join(lu_2)
        wc = WordCloud(font_path = font).generate(text)
        plt.figure('3')
        plt.imshow(wc , interpolation='bilinear')
        plt.title('数据挖掘-岗位职责词云')
        plt.axis("off")
        plt.show()

        # 岗位要求
        lu_1 = list(df_1.岗位要求.unique())
        lu_2 = list(df_2.岗位要求.unique())

        rpl = re.compile(r'、|\n|,|，|；|。|[1-9]')
        lu_1 = [rpl.sub("",item) for item in lu_1]
        lu_2 = [rpl.sub("",item) for item in lu_2]

        lu_1 = [",".join(jieba.cut(item)) for item in lu_1]
        lu_2 = [",".join(jieba.cut(item)) for item in lu_2]
        

        font = "font\\simhei.ttf"
        
        text = "".join(lu_1)
        wc = WordCloud(font_path = font).generate(text)
        plt.figure('1')
        plt.imshow(wc , interpolation='bilinear')
        plt.title('数据分析-岗位要求词云')
        plt.axis("off")
        plt.show()

        text = "".join(lu_2)
        wc = WordCloud(font_path = font).generate(text)
        plt.figure('3')
        plt.imshow(wc , interpolation='bilinear')
        plt.title('数据挖掘-岗位要求词云')
        plt.axis("off")
        plt.show()


    # 数据分析和数据挖掘-各公司岗位数分析
    if(describe_opt == "compjobs"):

        lst_1 = df_1.公司名.to_list()
        lst_2 = df_2.公司名.to_list()

        se_1 = set(lst_1)
        se_2 = set(lst_2)

        rpl = re.compile('（|）|北京|深圳|有限|责任|科技|公司|网络|信息|技术|集团|股份')
        dic_1 = {key:lst_1.count(key) for key in se_1}
        dic_lst_sorted = sorted(dic_1.items(),key=lambda x:x[1],reverse= True)[:10]
        dic_1 = {rpl.sub("",tup[0]):tup[1] for tup in dic_lst_sorted}
        dic_2 = {key:lst_2.count(key) for key in se_2}
        dic_lst_sorted = sorted(dic_2.items(),key=lambda x:x[1],reverse= True)[:10]
        dic_2 = {rpl.sub("",tup[0]):tup[1] for tup in dic_lst_sorted}

        x = np.arange(len(dic_1))
        
        # 数据分析岗
        y_1 = dic_1.values()
        compname = list(dic_1.keys())

        plt.figure('1', facecolor='lightgray')
        a = plt.bar(x , y_1 , 0.4 ,  color='dodgerblue' , align='center')

        for i in a:
            h = i.get_height()
            plt.text(i.get_x() + i.get_width() / 2, h, '%d' % int(h), ha='center', va='bottom')

        plt.tick_params(labelsize=8)
        plt.xticks(x,compname)

        plt.grid(linestyle=':', axis='y')
        plt.title('发布岗位最多的几家公司（数据分析岗）',fontsize=16)
        plt.xlabel('企业',fontsize=16)
        plt.ylabel('岗位数',fontsize=16)
        plt.show()

        # 数据挖掘岗
        y_2 = dic_2.values()
        compname = list(dic_2.keys())

        plt.figure('2', facecolor='lightgray')
        a = plt.bar(x , y_2 , 0.4 ,  color='dodgerblue' , align='center')

        for i in a:
            h = i.get_height()
            plt.text(i.get_x() + i.get_width() / 2, h, '%d' % int(h), ha='center', va='bottom')

        plt.tick_params(labelsize=8)
        plt.xticks(x,compname)

        plt.grid(linestyle=':', axis='y')
        plt.title('发布岗位最多的几家公司（数据挖掘岗）',fontsize=16)
        plt.xlabel('企业',fontsize=16)
        plt.ylabel('岗位数',fontsize=16)
        plt.show()

    # 数据分析和数据挖掘-公司领域分析
    if(describe_opt == "compfield"):

        # 公司名去重

        df_1 = df_1.drop_duplicates('公司名',inplace = False)
        df_2 = df_2.drop_duplicates('公司名',inplace = False)

        # 词云
        lst_1 = df_1.公司领域.to_list()
        lst_2 = df_2.公司领域.to_list()

        lu_1 = list(df_1.公司领域)
        lu_1 = [item +',' for item in lu_1]
        lu_2 = list(df_2.公司领域)
        lu_2.remove(nan)
        lu_2 = [item +',' for item in lu_2]

        font = "font\\simhei.ttf"
        
        text = "".join(lu_1)
        wc = WordCloud(font_path = font).generate(text)
        plt.figure('1')
        plt.imshow(wc , interpolation='bilinear')
        plt.title('数据分析-公司领域词云')
        plt.axis("off")
        plt.show()

        text = "".join(lu_2)
        wc = WordCloud(font_path = font).generate(text)
        plt.figure('2')
        plt.imshow(wc , interpolation='bilinear')
        plt.title('数据挖掘-公司领域词云')
        plt.axis("off")
        plt.show()


    # 数据分析和数据挖掘-公司规模分析
    if(describe_opt == "compsize"):

        ## 公司名去重

##        df_1 = df_1.drop_duplicates('公司名',inplace = False)
##        df_2 = df_2.drop_duplicates('公司名',inplace = False)

        lst_1 = df_1.公司人数.to_list()
        lst_2 = df_2.公司人数.to_list()

        compsize_lst = ["['15']","['15', '50']","['50', '150']",
                        "['150', '500']","['500', '2000']", "['2000']"]

        dic_1 = {key:lst_1.count(key) for key in compsize_lst}
        dic_2 = {key:lst_2.count(key) for key in compsize_lst}

        x = np.arange(len(dic_1))
        y_1 = dic_1.values()
        y_2 = dic_2.values()
        compsize = list(dic_1.keys())
        compsize = ["15人以下","15-50人","50-150人",
                        "150-500人","500-2000人", "2000人以上"]

        plt.figure('', facecolor='lightgray')
         
        a = plt.bar(x-0.2 , y_1 , 0.4 ,  color='dodgerblue' , label="数据分析", align='center')
        b = plt.bar(x+0.2 , y_2 , 0.4 ,  color='orangered' , label="数据挖掘", align='center')

        for i in a + b:
            h = i.get_height()
            plt.text(i.get_x() + i.get_width() / 2, h, '%d' % int(h), ha='center', va='bottom')

        plt.tick_params(labelsize=10)
        plt.xticks(x,compsize)
        plt.grid(linestyle=':', axis='y')
        plt.title('公司规模分布图',fontsize=16)
        plt.xlabel('公司人数',fontsize=16)
        plt.ylabel('公司数',fontsize=16)
        
        plt.legend()
        plt.show()

        
## 相关性分析（以拉勾网站为例）

if(ana_opt == "relate"):

    df_1 = df_lagou_fenxi # 数据分析岗位
    df_2 = df_lagou_wajue[:df_1.shape[0]] # 数据挖掘
        
    relate_opt = "diff_of_field"
    
    # 工资与学历和工作经验是否有关（以数据分析岗位为例）
    if(relate_opt == "sal_edu_exp"):

        df_1 = df_1.loc[:,('最低工资','最高工资','学历','工作年限')]
        s_1_avgsal = (df_1.最低工资 + df_1.最高工资)/2
        df_1['平均工资'] = s_1_avgsal

        aa = list(df_1.平均工资.unique())
        aa.sort() # 查看工资范围

        s_edu = df_1.groupby('学历').mean().平均工资
        s_exp = df_1.groupby('工作年限').mean().平均工资

        # 工资与学历的关系

        x = ['不限', '大专', '本科', '硕士', '博士']

        #折线图（平均值）
        dic = {item:s_edu[item] for item in x}

        plt.figure('1')
        plt.plot(list(dic.keys()),list(dic.values()),\
                 color="darkblue",linewidth=3,linestyle='--', marker='+',ms=10)
        plt.xlabel('学历',fontsize=16)
        plt.ylabel('薪资',fontsize=16)
        plt.title('薪资-学历关系图（数据分析岗）',fontsize=16)
        plt.show()

        #分布图
        bins = np.arange(0,80,5)
        
        plt.figure('2', facecolor='lightgray')
        for i in range(df_1.学历.unique().shape[0]):
            
            s = df_1.平均工资[df_1.学历 == x[i]]
            plt.hist(s, bins,  alpha=0.5,label = x[i])

        plt.grid(linestyle=':', axis='y')
        plt.title('不同学历工资分布图',fontsize=16)
        plt.xlabel('月薪(k)',fontsize=16)
        plt.ylabel('公司数',fontsize=16)
        plt.legend()
        plt.xlim(0,80)

        plt.show()


        # 工资与工作经验的关系

        x_1 = ['(0,0)', '(0,1)', '(1,3)', '(3,5)', '(5,10)', '(10,10)']
        x_2 = ['不限', '1年以下', '1-3年', '3-5年', '5-10年', '10年以上']

        #折线图（平均值）
        dic = {item:s_exp[item] for item in x_1}

        plt.figure('3')
        plt.plot(x_2,list(dic.values()),\
                 color="goldenrod",linewidth=3,linestyle=':', marker='*',ms=10)
        plt.xlabel('工作经验',fontsize=16)
        plt.ylabel('薪资',fontsize=16)
        plt.title('薪资-工作经验关系图（数据分析岗）',fontsize=16)
        plt.show()

        #分布图
        bins = np.arange(0,80,5)
        
        plt.figure('4', facecolor='lightgray')
        for i in range(df_1.工作年限.unique().shape[0]):
            
            s = df_1.平均工资[df_1.工作年限 == x_1[i]]
            plt.hist(s, bins,  alpha=0.5,label = x_2[i])

        plt.grid(linestyle=':', axis='y')
        plt.title('不同工作经验工资分布图',fontsize=16)
        plt.xlabel('月薪(k)',fontsize=16)
        plt.ylabel('公司数',fontsize=16)
        plt.legend()
        plt.xlim(0,80)

        plt.show()

    # 对领域进行分类，分析不同领域的差异，或者说岗位需求量与领域的关系（以数据分析为例）
    if(relate_opt == "diff_of_field"):

        se = set(re.split(",| ",",".join(list(df_1.公司领域.unique()))))
        lst = df_1.公司领域.to_list()
        dic = {item :len([1 for i in lst if(re.match(item,i))]) for item in se}

        dic['医疗健康'] += dic['医疗丨健康']
        dic.pop('医疗丨健康')

        dic['数据服务'] += dic['企业服务']
        dic.pop('企业服务')

        dic['电商'] += dic['电子商务']
        dic.pop('电子商务')

        dic = dict([item for item in dic.items() if(item[1]>5)])
        dic = {item[0]:item[1] for item in sorted(dic.items(),key = lambda x: x[1])}

        plt.pie(dic.values(), labels=dic.keys(), labeldistance=1.1, autopct='%1.1f%%')
        plt.title('各领域岗位数占比',fontsize=16)
        plt.show()

##        # 领域字符串转成向量并聚类
##        vec_lst = []
##        for w in lst:
##            vec_lst.append([1 if(re.match(item,w)) else 0 for item in se])
##
##        X = np.array(vec_lst)
##        model = KMeans(n_clusters = 5,random_state = 0)
##        y = model.fit_predict(X)
##
##        lst_0 = [lst[i] for i in range(len(lst)) if 0 == y[i]]
##        lst_1 = [lst[i] for i in range(len(lst)) if 1 == y[i]]
##        lst_2 = [lst[i] for i in range(len(lst)) if 2 == y[i]]
##        lst_3 = [lst[i] for i in range(len(lst)) if 3 == y[i]]
##        lst_4 = [lst[i] for i in range(len(lst)) if 4 == y[i]]


## 拉勾和猎聘对比分析（以数据分析岗位为例）

if(ana_opt == "compare"):

    df_1 = df_lagou_fenxi # 拉勾网数据分析岗位
    df_2 = df_liepin_fenxi # 猎聘网数据分析岗位
    df_1 = df_1[:df_2.shape[0]]

    compare_opt = "exp"

    # 两个网站工资分布对比
    if(compare_opt == "sal"):

        s_1_avgsal = (df_1.最低工资 + df_1.最高工资)/2
        s_2_avgsal = (df_2.最低工资 + df_2.最高工资)/2

        a = list(s_1_avgsal.unique())
        b = list(s_2_avgsal.unique())

        bins = np.arange(0,80,5)

        plt.figure('', facecolor='lightgray')
        
        plt.hist(s_1_avgsal,bins,color='steelblue',alpha=0.5,label='拉勾网')
        plt.hist(s_2_avgsal,bins,color='fuchsia',alpha=0.5,label='猎聘网')

        plt.grid(linestyle=':', axis='y')
        plt.title('工资分布图',fontsize=16)
        plt.xlabel('月薪(k)',fontsize=16)
        plt.ylabel('岗位数',fontsize=16)
        plt.legend()
        plt.xlim(0,80)

        plt.show()

    # 两个网站学历分布对比
    if(compare_opt == "edu"):

        lst_1 = df_1.学历.to_list()
        lst_2 = df_2.学历.to_list()

        edu_lst = ['不限', '大专', '本科', '硕士', '博士']

        dic_1 = {key:lst_1.count(key) for key in edu_lst}
        dic_2 = {key:lst_2.count(key) for key in edu_lst}

        x = np.arange(len(dic_1))
        y_1 = dic_1.values()
        y_2 = dic_2.values()
        edu = list(dic_1.keys())

        plt.figure('', facecolor='lightgray')
         
        a = plt.bar(x-0.2 , y_1 , 0.4 ,  color='dodgerblue' , label="拉勾网", align='center')
        b = plt.bar(x+0.2 , y_2 , 0.4 ,  color='orangered' , label="猎聘网", align='center')

        for i in a + b:
            h = i.get_height()
            plt.text(i.get_x() + i.get_width() / 2, h, '%d' % int(h), ha='center', va='bottom')

        plt.tick_params(labelsize=10)
        plt.xticks(x,edu)
        plt.grid(linestyle=':', axis='y')
        plt.title('学历分布图',fontsize=16)
        plt.xlabel('学历',fontsize=16)
        plt.ylabel('岗位数',fontsize=16)
        
        plt.legend()
        plt.show()

    # 两个网站工作年限分布对比
    if(compare_opt == "exp"):

        s = df_2.工作年限
        s = s.replace({0:'(0,1)',1:'(1,3)',2:'(1,3)',3:'(3,5)',4:'(3,5)',5:'(5,10)',\
                       6:'(5,10)',7:'(5,10)',8:'(5,10)',10:'(10,10)'})
        
        df_2.工作年限 = s
        
        lst_1 = df_1.工作年限.to_list()
        lst_2 = df_2.工作年限.to_list()

        exp_lst = ['(0,0)', '(0,1)', '(1,3)', '(3,5)', '(5,10)','(10,10)']

        dic_1 = {key:lst_1.count(key) for key in exp_lst}
        dic_2 = {key:lst_2.count(key) for key in exp_lst}

        x = np.arange(len(dic_1))
        y_1 = dic_1.values()
        y_2 = dic_2.values()
        exp = list(dic_1.keys())
        exp = ['不限', '1年以下', '1-3年', '3-5年', '5-10年', '10年以上']

        plt.figure('', facecolor='lightgray')
         
        a = plt.bar(x-0.2 , y_1 , 0.4 ,  color='dodgerblue' , label="拉勾网",align='center')
        b = plt.bar(x+0.2 , y_2 , 0.4 ,  color='orangered' , label="猎聘网",align='center')

        for i in a + b:
            h = i.get_height()
            plt.text(i.get_x() + i.get_width() / 2, h, '%d' % int(h), ha='center', va='bottom')

        plt.tick_params(labelsize=10)
        plt.xticks(x,exp)

        plt.grid(linestyle=':', axis='y')
        plt.title('工作年限分布图',fontsize=16)
        plt.xlabel('工作年限',fontsize=16)
        plt.ylabel('岗位数',fontsize=16)
        plt.legend()
        plt.show()
    
    
        
