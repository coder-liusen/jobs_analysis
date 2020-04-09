
'''

功能：猎聘网职位信息 爬取、解析、保存
注意：（1）猎聘网是静态网站；（2）它有反爬

'''


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time


###############################################################
# 从文件中读取请求参数，以字典形式保存

def getRequestParams(query_dir,job_name = "数据分析",area_code = "010"):

    with open(query_dir,'r') as f:
        s = f.read()
    
    param_dic = eval(s)
    param_dic['queryparams']['key'] = job_name
    param_dic['queryparams']['dqs'] = str(area_code)

    return param_dic


###############################################################
# 从一个职位信息标签中解析出各项职位信息，以字典形式保存

def getJobInformation(job):

    #解析公司名称
    try:
        companyname = ''.join(job.find('p','company-name').find('a').contents)
    except:
        companyname = ""
    else:
        print(companyname)
        
    #解析公司领域或融资情况
    try:
        field = job.find('p','field-financing').find('span')
        if (field.find('a') != None):
            field = field.find('a') # 注意，该项信息有的在span中，有的在a中
        companyfield = ''.join(field.contents).strip()
    except:
        companyfield = ""

    #解析招聘岗位
    try:
        position = ''.join(job.find('h3').find('a').contents).strip()
    except:
        position = ""

    
    #解析招聘薪资、公司位置、学历、工作年限
    try:
        infos = job.find('p','condition clearfix')['title'].split('_')
    except:
        infos = ""

    #使用切片，而不是直接使用下标，是因为当infos为空字符串时，
    #切片方式能返回空字符串，下标方式则会报错    
    salary = infos[0:1] 
    place = infos[1:2]
    education = infos[2:3]
    workyear = infos[3:4]

    #解析发布时间
    try:
        createdate = job.find('time')['title']
    except:
        createdate = ""

    #解析职位详情链接
    try:
        pos_href = job.find('h3').find('a')['href']
    except:
        pos_href = ""
    else:
        if(re.match("https",pos_href) is None):
            pos_href = ""
##        print(pos_href)
    
    #整成一个字典
    jobInfo = {'companyname':companyname,
                    'companyfield':companyfield,
                    'position':position,
                    'salary':salary,
                    'place':place,
                    'education':education,
                    'workyear':workyear,
                    'createdate':createdate,
                    'url':pos_href
                   }
    
    return jobInfo


###############################################################
# 发送get请求，获取当前页内容，为html格式字符串

def getcurPageHtml(requestParams,ipage):

    # 获取完整的请求参数
    param_curPage = {'curPage':str(ipage)}
    params = dict(requestParams['queryparams'],**param_curPage)

    # 向目标网站发送get请求，并接收返回结果
    
    s = requests.Session() # 维持会话
    s.get(requestParams['url'],params = params,headers = requestParams['headers'])
    cookies_get = s.cookies

    res = requests.post(requestParams['url'],
                        params = params,
                        headers = requestParams['headers'],
                        cookies=cookies_get ,
                        timeout = 5) # get和post没有本质区别
                                                           
    return res.text


###############################################################
#  解析岗位职责和岗位要求

def parse_JobDetail(poition_url,requestParams_dic):

    try:
        html = requests.get(poition_url,headers = requestParams_dic['headers'])
        soup = BeautifulSoup(html.text,'lxml')
        detail = str(soup.find('div','content content-word'))
        compfiled = str(soup.find('ul','new-compintro').find('a')['title'])
        compsize = str(soup.find('ul','new-compintro').find_all('li')[1])
        compsize = re.findall(r'(\d+)',compsize)
    except:
        detail = ""
        compfiled = ""
        compsize = []

    # 去掉所有标签
    detail = re.sub('<.*?>','',detail)
    detail_lst = re.split("[:：]",detail)
    sa = "".join(detail_lst[1:2]).strip()[:-4] # 为避免用下标取元素可能取不到而报错，采用切片取元素
    sb = "".join(detail_lst[2:3]).strip() #  为避免用下标取元素可能取不到而报错，采用切片取元素

    return sa,sb,compfiled,compsize
    
    
###############################################################
# 请求页面 -> 解析职位标签 -> 提取职位信息并保存

def get_AllJobInformation(query_dir,job_name,area_code,page_num,sleep_timeinc,csv_name):

    # 声明各项职位信息列表
    companyname_list = []
    companyfield_list = []
    position_list = []
    salary_list = []
    place_list = []
    education_list = []
    workyear_list = []
    createdate_list = []

    positionResponse_list = []
    positionNeed_list = []
    companysize_list = []

    # 获取请求参数
    requestParams_dic = getRequestParams(query_dir,job_name,area_code)

    # 请求页面、获取职位信息标签、解析职位信息
    pageList = range(page_num)
    
    for ipage in pageList:

        print("猎聘 - 抓取第 %d 页" %(ipage+1))
        try:
            html = getcurPageHtml(requestParams_dic,ipage) #请求html页面
            soup = BeautifulSoup(html,'lxml') #将html转成BeautifulSoup对象
            job_tag_list = soup.find('ul','sojob-list').find_all('li') #提取职位标签
        except:
            input('please varify on the web and confirm by input \'OK\':')
            html = getcurPageHtml(requestParams_dic,ipage) #继续请求html页面
            soup = BeautifulSoup(html,'lxml') #将html转成BeautifulSoup对象
            job_tag_list = soup.find('ul','sojob-list').find_all('li') #提取职位标签
        else:
            pass
            
        for job_tag in job_tag_list:

            jobInformation_dic = getJobInformation(job_tag) #从职位标签中获取职位信息，以字典形式保存
            
            companyname_list.append(jobInformation_dic['companyname'])
##            companyfield_list.append(jobInformation_dic['companyfield'])
            position_list.append(jobInformation_dic['position'])
            salary_list.append(jobInformation_dic['salary'])
            place_list.append(jobInformation_dic['place'])
            education_list.append(jobInformation_dic['education'])
            workyear_list.append(jobInformation_dic['workyear'])
            createdate_list.append(jobInformation_dic['createdate'])

            # 解析岗位详情
            url_get = jobInformation_dic['url']
            sa,sb,sc,sd = parse_JobDetail(url_get,requestParams_dic)
            positionResponse_list.append(sa)
            positionNeed_list.append(sb)
            companyfield_list.append(sc)
            companysize_list.append(sd)
            
        time.sleep(sleep_timeinc)
 

    # 将职位信息保存到.csv文件 
    jobInformation_df = pd.DataFrame({
        '公司名':companyname_list,
        '公司领域':companyfield_list,
         '招聘岗位':position_list,
         '薪资':salary_list,
         '公司位置':place_list,
         '学历':education_list,
        '工作年限':workyear_list,
        '发布时间':createdate_list,
        '岗位职责':positionResponse_list,
        '岗位要求':positionNeed_list,
        '公司人数':companysize_list
        })
    jobInformation_df.to_csv(csv_name)


###############################################################
    
if __name__ == "__main__":

    query_param_dir = "F:\\python_code\\analysis\\web_info\\liepin_query.txt" # 请求参数文件
    job_name = "数据分析" # 职位名
    area_code = "010" # 地区代码（注意不一定是区号）
    page_num = 10 # 抓取页面个数
    sleep_timeinc = 5 # 每次抓取页面之间休眠间隔
    csv_name = "data\\liepin_jobs_"+job_name+"_"+ \
               area_code+"_"+str(page_num)+".csv" # 保存职位信息的文件名
    
    get_AllJobInformation(query_param_dir,job_name,area_code,page_num,sleep_timeinc,csv_name)


