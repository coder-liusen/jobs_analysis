# -*- coding: utf-8 -*-

'''
功能：拉勾网职位数据 爬取、解析、保存

'''

import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

###############################################################
# 汉字按utf-8 网页编码

def url_encode(s):

    return "%".join(str(s.encode('utf-8')).strip('b').strip('\'').split('\\x'))


###############################################################
# 从文件中读取请求参数，以字典形式保存

def getRequestParams(query_param_dir,job_name,area_name):

    with open(query_param_dir,'r') as f:
        s = f.read()

    param_dic = eval(s)
    param_dic['headers_post']['Referer'] = param_dic['headers_post']['Referer'].replace("$zhiwei$",url_encode(job_name))
    param_dic['url_get'] = param_dic['url_get'].replace("$zhiwei$",url_encode(job_name))
    param_dic['formdata']['kd'] = job_name
    param_dic['url_post'] = param_dic['url_post'].replace("$diqu$",url_encode(area_name))
 
    return param_dic

    
###############################################################
# 发送post请求，获取当前页内容，为json规范的字符串

def getcurPageText(requestParams,ipage):
    
    formdata_curPage = {'pn':str(ipage)}
    formdata = dict(requestParams['formdata'],**formdata_curPage)

    s = requests.Session() # 维持会话
    s.get(requestParams['url_get'],headers = requestParams['headers_get']) 
    cookies_get = s.cookies

    res_post = requests.post(requestParams['url_post'],headers = requestParams['headers_post'],\
                             cookies = cookies_get,data = formdata)
    res_post.encoding = res_post.apparent_encoding

    return res_post.text

    
###############################################################
#  解析岗位职责和岗位要求

def parse_JobDetail(poition_url,requestParams_dic):

    headers_get =  requestParams_dic['headers_get']
    html = requests.get(poition_url,headers = headers_get)
    print(len(html.text))
    soup = BeautifulSoup(html.text,'lxml')
    detail = str(soup.find('div','job-detail')) # 获取岗位职责和岗位要求文本

    # 去掉所有标签
    detail = re.sub('<.*?>','',detail)
    detail_lst = re.split("[:：]",detail)
    sa = "".join(detail_lst[1:2]).strip()[:-4] # 为避免用下标取元素可能取不到而报错，采用切片取元素
    sb = "".join(detail_lst[2:3]).strip() #  为避免用下标取元素可能取不到而报错，采用切片取元素

    print('<岗位职责：>\n',sa)
    print('<岗位要求：>\n',sb)

    return sa,sb
    
   
###############################################################
# 获取并保存全部职位信息

def get_AllJobInformation(query_param_dir,job_name,area_name,page_num,sleep_timeinc,csv_name):

    # 声明各项职位信息列表
    companyname_list = []
    city_list = []
    cmpanysize_list = []
    industryfield_list = []
    positionName_list = []
    createdate_list = []
    salary_list = []
    workyear_list = []
    education_list = []

    positionResponse_list = []
    positionNeed_list = []

    # 获取请求参数
    requestParams_dic = getRequestParams(query_param_dir,job_name,area_name)

    # 请求页面、获取职位信息标签、解析职位信息
    pageList = range(1,page_num+1)
    
    for ipage in pageList:

        print("拉钩 - 抓取第 %d 页..." %(ipage))
        
        Text = getcurPageText(requestParams_dic,ipage)
        JsonData = json.loads(Text)
        
        jobinfo_list = JsonData["content"]["positionResult"]["result"]

        for job_dic in jobinfo_list:

            companyname_list.append(job_dic['companyFullName'])
            city_list.append(job_dic['city'])
            cmpanysize_list.append(job_dic['companySize'])
            industryfield_list.append(job_dic['industryField'])
            positionName_list.append(job_dic['positionName'])
            createdate_list.append(job_dic['createTime'])
            salary_list.append(job_dic['salary'])
            workyear_list.append(job_dic['workYear'])
            education_list.append(job_dic['education'])

            print(job_dic['companyFullName'])

            # 解析岗位职责和岗位要求
            poition_url = 'https://www.lagou.com/jobs/' + \
                          str(job_dic['positionId']) + \
                          '.html'

            sa,sb = parse_JobDetail(poition_url,requestParams_dic)
            positionResponse_list.append(sa)
            positionNeed_list.append(sb)

            time.sleep(sleep_timeinc) # 否则会有大量抓不到的网页
            
    # 将职位信息保存到.csv文件
    end_res = pd.DataFrame({
        '公司名':companyname_list,
        '城市':city_list,
         '公司人数':cmpanysize_list,
         '公司领域':industryfield_list,
         '职位':positionName_list,
         '发布时间':createdate_list,
        '工资':salary_list,
        '工作年限':workyear_list,
        '学历':education_list,
        '岗位职责':positionResponse_list,
        '岗位要求':positionNeed_list
        })
    
    end_res.to_csv(csv_name)
            


if __name__ == "__main__":

    query_param_dir = "F:\\python_code\\analysis\\web_info\\lagou_query.txt" # 请求网页的参数文件
    job_name = "数据分析" # 职位名
    area_name = "北京" # 地区名
    page_num = 100 # 抓取页面个数
    sleep_timeinc = 10 # 每次抓取页面之间休眠间隔
    csv_name = "data\\lagou_jobs_"+job_name+"_"+\
               area_name+"_"+str(page_num)+".csv" # 保存职位信息的文件名
    
    get_AllJobInformation(query_param_dir,job_name,area_name,page_num,sleep_timeinc,csv_name)

