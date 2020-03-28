import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
from random import randint
import pandas as pd

from selenium.webdriver.chrome.options import Options


def my_to_csv(all_target_content):
    # 篩選標準 先隨便選
    tmp_data = all_target_content[0][0].split('\n')
    columns = []
    for i in range(len(tmp_data)):
        columns.append(tmp_data[i].split(':')[0])
    columns = columns[:-1]
    file_list = all_target_content
    data = []
    for file_name in file_list:
        tmp_data = file_name[0].split('\n')
        tmp_columns = []
        for i in range(len(tmp_data)):
            tmp_columns.append(tmp_data[i].split(':')[0])
        tmp_columns = tmp_columns[:-1]
        tmp_data = tmp_data[:-1]
        if tmp_columns == columns:
            data.append(tmp_data)
        else: # 把不同欄挑出一樣的合併
            tmp2_data = []
            for j in range(len(tmp_columns)):
                if tmp_columns[j] in columns:
                    tmp2_data.append(tmp_data[j])
            data.append(tmp2_data)
    # print(data)
    df = pd.DataFrame(data=data, columns=columns)
    print(df)
    lambda s: s.split(': ')[-1]

    def column_filter(s):
        output = s.split(': ')[-1]
        return output
    for i in columns:
        df[i] = df[i].apply(column_filter)
    df.to_csv('./try_104.csv', index=0, encoding = 'utf_8_sig')
    ok = 'OK'
    return ok



# 這邊設定driver不顯示，chrome_options=chrome_options這個設定在下面
chrome_options = Options()
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)

# https://www.104.com.tw/jobs/search/?ro=1&keyword=資料科學家&area=6001001000&isnew=30&page=1&mode=l&order=11&jobsource=2018indexpoc
# https://www.104.com.tw/jobs/search/?ro=1&isnew=30&kwop=1&keyword=資料工程師&area=6001001000&order=11&asc=0&page=1&mode=l&jobsource=2018indexpoc

url = 'https://www.104.com.tw/jobs/search/?ro=0&isnew=3&kwop=1&keyword=資料工程師&area=6001001000&order=11&asc=0&page=1&mode=l&jobsource=2018indexpoc'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
# 限定全職的工作，如果不限定則輸入0,想要查詢的關鍵字,限定在台北的工作,只要最近一個月有更新的過的職缺,清單的瀏覽模式'mode':'l',kwop=1=是否全部keyword都要比對
"""
res = requests.get(url, my_params, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
# print(soup.prettify())
title = soup.select('em[class="b-txt--highlight"]')
print(title[0].prettify())
"""
all_target_content = []
page = 1
k = 0
k2 = 0
while page > 0:
    url = 'https://www.104.com.tw/jobs/search/?ro=0&isnew=3&kwop=1&keyword=資料工程師&area=6001001000&order=11&asc=0&page=%d&mode=l&jobsource=2018indexpoc' %page
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # print(soup.prettify())
    title = soup.select('li[class="job-mode__jobname"] a')
    if title == []:
        break
    # 多個title及url，iter_com抓第幾個公司名稱
    iter_com = 1
    for t in title:
        company_catch = soup.select('li[class="job-mode__company"]')
        target_company = company_catch[iter_com].text.replace('\n','')
        iter_com += 1
        target_title = t.text
        target_url = 'https:' + t['href']
        # 標提 及 網址 及 公司名稱 放入
        target_content = '工作標題: ' + target_title + '\n'
        target_content += '工作網址: ' + target_url + '\n'
        target_content += '公司名稱: ' + target_company + '\n'
        # 將標題換成可存字元
        rem_p = re.compile(r'[~\ \-,$()#+&*?.】【/]')
        target_title = re.sub(rem_p, "_", target_title)
        # 等等放要抓的東西
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(target_url)
        html = driver.page_source # 取得html文字
        driver.close()
        target_content_soup = BeautifulSoup(html, 'html.parser')
        # 工作內容
        target_content += '工作內容: '+target_content_soup.select('p[class="mb-5 r3 job-description__content text-break"]')[0].text.replace('\r', '。').replace('\n', ';')+'\n'
        a = target_content_soup.select('div[class="row mb-2"]')
        for detail_inverse in range(len(a)):
            delimiter = ''
            try:
                target_content += a[detail_inverse].text.split()[0]+': '+delimiter.join(a[detail_inverse].text.split()[1:])+'\n'
            except:
                pass
        print(target_content)
        print(k)
        k = k+1
        all_target_content.append([target_content])
    print(my_to_csv(all_target_content))
    time.sleep(randint(1, 5))
    page = page + 1
print(all_target_content)