import requests
from bs4 import BeautifulSoup
import json
import pprint
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
one_adjx_url = 'https://www.104.com.tw/job/ajax/content/6maa7'
# print(one_titlename)
# print(one_url)
# print(one_adjx_url)
target_url = one_adjx_url
target_res = requests.get(target_url, headers=headers)
target_soup = BeautifulSoup(target_res.text, 'html.parser').text
jdata = json.loads(target_soup)
def istype(data):
    str_join = ','
    a = ''
    if (type(data).__name__ == 'str') | (type(data).__name__ == 'dict'):
        a = data
    elif data==[]:
        a = '不拘'
    elif type(data[0]).__name__ == 'str':
        a = str_join.join(data)
    else:
        for i in range(len(data)):
            a = a + data[i]['description'] + ','
        a = a[:-1]
    return a


list1 = ['工作名稱', '公司名稱', '職務類別', '上班地點', '薪資',
         '上班時間', '更新日期', '接受身分', '學歷要求', '工作經歷',
         '科系要求', '語言要求', '擅長工具', '休假制度', '需求人數',
         '工作內容', '其他條件', '福利制度', '聯絡人eamil']
list2 = [
    istype(jdata['data']['header']['jobName']),
    istype(jdata['data']['header']['custName']),
    istype(jdata['data']['jobDetail']['jobCategory']),
    istype(jdata['data']['jobDetail']['addressRegion'])+istype(jdata['data']['jobDetail']['addressDetail']),
    istype(jdata['data']['jobDetail']['salary']),
    istype(jdata['data']['jobDetail']['workPeriod']),
    istype(jdata['data']['header']['appearDate']),
    istype(jdata['data']['condition']['acceptRole']['role'][0]['description']),
    istype(jdata['data']['condition']['edu']),
    istype(jdata['data']['condition']['workExp']),
    istype(jdata['data']['condition']['major']),
    istype(jdata['data']['condition']['language']),
    istype(jdata['data']['condition']['specialty']),
    istype(jdata['data']['jobDetail']['vacationPolicy']),
    istype(jdata['data']['jobDetail']['needEmp']),
    istype(jdata['data']['jobDetail']['jobDescription'].replace('\r', '').replace('\n', '')),
    istype(jdata['data']['condition']['other'].replace('\r', '').replace('\n', '')),
    istype(jdata['data']['welfare']['welfare'].replace('\r', '').replace('\n', '')),
    istype(jdata['data']['contact']['hrName']) + ',' + istype(jdata['data']['contact']['email']).replace('', '無填寫email')
]

one_dict = dict(zip(list1, list2))
print(pd.DataFrame(one_dict, index=[0]))

"""
list1=[jdata['data']['header']['custName'],jdata['data']['header']['appearDate']]
list2=['公司名稱','更新日期']
dict(zip(list2,list1))

"""