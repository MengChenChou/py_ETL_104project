import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
from random import randint
# https://www.104.com.tw/jobs/search/?ro=1&keyword=資料科學家&area=6001001000&isnew=30&page=1&mode=l&order=11
import os
resource_path = r'./try_104'
if not os.path.exists(resource_path):
    os.mkdir(resource_path)


url = 'https://www.104.com.tw/jobs/search/?'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
# 限定全職的工作，如果不限定則輸入0,想要查詢的關鍵字,限定在台北的工作,只要最近一個月有更新的過的職缺,清單的瀏覽模式'mode':'l',kwop=1
my_params = {'ro':'1',
             'keyword':'資料科學家',
             'area':'6001001000',
             'isnew':'30',
             'page':'1',
             'mode':'l',
             'order':'11'}
"""
res = requests.get(url, my_params, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
# print(soup.prettify())
title = soup.select('em[class="b-txt--highlight"]')
print(title[0].prettify())
"""
page = 2
k = 0
k2 = 0
while page > 0:
    my_params = {'ro': '1',
                 'keyword': '資料科學家',
                 'area': '6001001000',
                 'isnew': '30',
                 'page': '%d' % page,
                 'mode': 'l',
                 'order': '11'}
    res = requests.get(url, my_params, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # print(soup.prettify())
    title = soup.select('li[class="job-mode__jobname"] a')
    if title == []:
        break
    # 多個title及url
    for t in title:
        company_catch = soup.select('li[class="job-mode__company"]')
        target_company = company_catch[1].text.replace('\n','')
        target_title = t.text
        target_url = 'https:' + t['href']
        # 標提 及 網址 及 公司名稱 放入
        target_content = '工作標題: ' + target_title + '\n'
        target_content += '工作網址: ' + target_url + '\n'
        target_content += '公司名稱: ' + target_company + '\n'
        # 將標題換成可存字元
        rem_p = re.compile(r'[~\ \-,$()#+&*?.\】\【/]')
        target_title = re.sub(rem_p, "_", target_title)
        # 等等放要抓的東西
        driver = webdriver.Chrome()
        driver.get(target_url)
        html = driver.page_source # 取得html文字
        driver.close()
        target_content_soup = BeautifulSoup(html, 'html.parser')
        # 工作內容
        target_content += '工作內容: '+target_content_soup.select('p[class="mb-5 r3 job-description__content text-break"]')[0].text.replace('\r', '。').replace('\n', ',')+'\n'
        a = target_content_soup.select('div[class="row mb-2"]')
        for detail_inverse in a:
            delimiter = ''
            target_content += detail_inverse.text.split()[0]+': '+delimiter.join(detail_inverse.text.split()[1:])+'\n'
        print(target_content)
        try:
            with open(r'%s/%s%s.txt' % (resource_path, target_title, target_company), 'w', encoding='utf-8') as w:
                w.write(target_content)
            print(k)
        except:
            pass
        k = k+1

    time.sleep(randint(1, 5))
    page = page + 1

