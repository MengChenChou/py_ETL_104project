import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
# 睡覺
import time
from random import randint

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
        try:
            for i in range(len(data)):
                a = a + data[i]['description'] + ','
            a = a[:-1]
        except:
            for j in range(len(data)):
                a = a + data[i]['language'] + data[i]['ability']
            a = a[:-1]

    return a
# 總dataframe
tmp_total_pd_dataframe = pd.DataFrame(columns=['工作名稱', '工作網址', '公司名稱', '職務類別', '上班地點',
                                               '薪資', '上班時間', '更新日期', '接受身分', '學歷要求',
                                               '工作經歷', '科系要求', '語言要求', '擅長工具', '休假制度',
                                               '需求人數', '工作內容', '其他條件', '福利制度', '聯絡人eamil'])

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
page = 1
while page > 0:
    url = 'https://www.104.com.tw/jobs/search/?ro=0&isnew=3&kwop=1&keyword=資料工程師&area=6001001000&order=11&asc=0&page=%d&mode=l&jobsource=2018indexpoc' % page
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup.prettify())
    title = soup.select('li[class="job-mode__jobname"] a')
    if title == []:
        break
    # 紀錄一頁的
    tmp_one_pd_dataframe = pd.DataFrame(columns=['工作名稱', '工作網址', '公司名稱', '職務類別', '上班地點',
                                                 '薪資', '上班時間', '更新日期', '接受身分', '學歷要求',
                                                 '工作經歷', '科系要求', '語言要求', '擅長工具', '休假制度',
                                                 '需求人數', '工作內容', '其他條件', '福利制度', '聯絡人eamil'])

    i = 1
    for t in title:
        one_titlename = t.text
        one_url = 'https:' + t['href']
        one_adjx_url = 'https://www.104.com.tw/job/ajax/content/' + one_url.replace('/', '?').split('?')[4]
        # print(one_titlename)
        # print(one_url)
        # print(one_adjx_url)
        target_url = one_adjx_url
        target_res = requests.get(target_url, headers=headers)
        target_soup = BeautifulSoup(target_res.text, 'html.parser').text
        jdata = json.loads(target_soup)
        list1 = ['工作名稱', '工作網址', '公司名稱', '職務類別', '上班地點',
                 '薪資', '上班時間', '更新日期', '接受身分', '學歷要求',
                 '工作經歷', '科系要求', '語言要求', '擅長工具', '休假制度',
                 '需求人數', '工作內容', '其他條件', '福利制度', '聯絡人eamil']
        list2 = [
            istype(jdata['data']['header']['jobName']),
            one_url,
            istype(jdata['data']['header']['custName']),
            istype(jdata['data']['jobDetail']['jobCategory']),
            istype(jdata['data']['jobDetail']['addressRegion']) + istype(jdata['data']['jobDetail']['addressDetail']),
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
            istype(jdata['data']['jobDetail']['jobDescription'].replace('\r', '').replace('\n', '').replace(':', ' ')),
            istype(jdata['data']['condition']['other'].replace('\r', '').replace('\n', '').replace(':', ' ')),
            istype(jdata['data']['welfare']['welfare'].replace('\r', '').replace('\n', '').replace(':', ' ')),
            istype(jdata['data']['contact']['hrName']) + ',' + istype(jdata['data']['contact']['email'])
        ]
        print(page)
        print(i)
        print('OK')
        i = i + 1
        one_dict = dict(zip(list1, list2))
        one_df = pd.DataFrame(one_dict, index=[0])
        tmp_one_pd_dataframe = pd.concat([tmp_one_pd_dataframe, one_df], axis=0)
    tmp_total_pd_dataframe = pd.concat([tmp_total_pd_dataframe, tmp_one_pd_dataframe], axis=0)
    tmp_total_pd_dataframe.to_csv('./try_104.csv', index=0, encoding='utf_8_sig')
    page = page + 1

"""

# 這邊是adjx_1
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
# print(soup.prettify())
title = soup.select('li[class="job-mode__jobname"] a')
tmp_one_pd_dataframe = pd.DataFrame(columns=['工作名稱', '公司名稱', '職務類別', '上班地點', '薪資',
                                             '上班時間', '更新日期', '接受身分', '學歷要求', '工作經歷',
                                             '科系要求', '語言要求', '擅長工具', '休假制度', '需求人數',
                                             '工作內容', '其他條件', '福利制度', '聯絡人eamil'])
i=1
for t in title:
    one_titlename = t.text
    one_url = 'https:' + t['href']
    one_adjx_url = 'https://www.104.com.tw/job/ajax/content/' + one_url.replace('/','?').split('?')[4]
    # print(one_titlename)
    # print(one_url)
    # print(one_adjx_url)
    target_url = one_adjx_url
    target_res = requests.get(target_url, headers=headers)
    target_soup = BeautifulSoup(target_res.text, 'html.parser').text
    jdata = json.loads(target_soup)
    list1 = ['工作名稱', '公司名稱', '職務類別', '上班地點', '薪資',
             '上班時間', '更新日期', '接受身分', '學歷要求', '工作經歷',
             '科系要求', '語言要求', '擅長工具', '休假制度', '需求人數',
             '工作內容', '其他條件', '福利制度', '聯絡人eamil']
    list2 = [
        istype(jdata['data']['header']['jobName']),
        istype(jdata['data']['header']['custName']),
        istype(jdata['data']['jobDetail']['jobCategory']),
        istype(jdata['data']['jobDetail']['addressRegion']) + istype(jdata['data']['jobDetail']['addressDetail']),
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
        istype(jdata['data']['jobDetail']['jobDescription'].replace('\r', '').replace('\n', '').replace(':', ' ')),
        istype(jdata['data']['condition']['other'].replace('\r', '').replace('\n', '').replace(':', ' ')),
        istype(jdata['data']['welfare']['welfare'].replace('\r', '').replace('\n', '').replace(':', ' ')),
        istype(jdata['data']['contact']['hrName']) + ',' + istype(jdata['data']['contact']['email'])
    ]
    print(i)
    print('OK')
    i=i+1
    one_dict = dict(zip(list1, list2))
    one_df = pd.DataFrame(one_dict, index=[0])
    tmp_one_pd_dataframe = pd.concat([tmp_one_pd_dataframe, one_df], axis=0)
tmp_one_pd_dataframe.to_csv('./try_104.csv', index=0, encoding='utf_8_sig')
"""