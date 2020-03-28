import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
target_url = "https://www.104.com.tw/job/6emjd?jobsource=n104bank2"
# https://m.104.com.tw/job/6roij?jobsource=n104bank2
# https://m.104.com.tw/job/6roij?jobsource=n104bank2
# https://m.104.com.tw/job/6khvh?jobsource=n104bank2
driver = webdriver.Chrome()
driver.get(target_url)
html = driver.page_source # 取得html文字
driver.close()
target_content_soup = BeautifulSoup(html, 'html.parser')
# 工作內容
target_content = '工作內容: '+target_content_soup.select('p[class="mb-5 r3 job-description__content text-break"]')[0].text.replace('\r', '。').replace('\n', ',')
print(target_content)
print('#################')
a = target_content_soup.select('div[class="row mb-2"]')
for detail_inverse in a:
    delimiter = ''
    print(detail_inverse.text.split()[0]+': '+delimiter.join(detail_inverse.text.split()[1:])+'\n')
"""
#print(target_content)
a = target_content_soup.select('div[class="row mb-2"]')
print(a[0].text.split('職務類別')[1].replace(' ',''))
#for detail_inverse in a:
    #print(a)
    #delimiter = ''
    #target_content += detail_inverse.text.split()[0]+': '+delimiter.join(detail_inverse.text.split()[1:])+'\n'

print('######################')
a = target_content_soup.select('div[class="row mb-2"]')
for detail_inverse in a:
    delimiter = ''
    target_content += detail_inverse.text.split()[0]+': '+delimiter.join(detail_inverse.text.split()[1:])+'\n'

print(target_content)
"""
"""
target_content += '推: %s\n' % (push_up)
target_content += '噓: %s\n' % (push_down)
target_content += '分數: %s\n' % (score)
target_content += '作者: %s\n' % (author)
target_content += '標題: %s\n' % (title)
target_content += '時間: %s\n' % (datetime)
"""




"""

#<p class="mb-5 r3 job-description__content text-break" data-v-2468802c="" data-v-52599d4b="">
# 17 Media is the.........
# [0]取出這個字串，.text取出文字
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36'}
target_detail_res = requests.get(target_url, headers=headers)
target_detail_soup = BeautifulSoup(target_detail_res.text, 'html.parser')
target_detail = target_detail_soup.select('div[class="content"]')
# 職務類別

#上班地點 #職務類別 #需求人數 #更新日期
print(target_detail[0].text.replace('\n', '').replace('\r', '').split()[0])
print('職務類別：'+target_detail[0].text.replace('\n', '').replace('\r', '').split()[2])
print(target_detail[0].text.replace('\n', '').replace('\r', '').split()[3])

# 工作待遇[0],公司福利[1]
print(target_detail[2].text.replace('\n', '').replace('\r', '').replace(' ', '').split("薪資行情")[0])
print(target_detail[2].text.replace('\n', '').replace('\r', '').replace(' ', '').split("薪資行情")[1])

# 上班時段 #休假制度
print(target_detail[3].text.replace('\n', ' ').split()[2] + target_detail[3].text.replace('\n', ' ').split()[3])
print(target_detail[3].text.replace('\n', ' ').split()[4] + target_detail[3].text.replace('\n', ' ').split()[5])

# 接受身分
print(target_detail[4].text.split()[0] + target_detail[4].text.split()[1])
#工作經驗 #學歷要求
print(target_detail[4].text.split()[4] + target_detail[4].text.split()[5])
print(target_detail[4].text.split()[6] + target_detail[4].text.split()[7])
"""
