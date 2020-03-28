import pandas as pd
import os

path = 'C:/Users/User/PycharmProjects/pyETL/work_104/try_104'#檔案的資料夾
os.listdir('./')
file_list = os.listdir(path)
print(file_list)
# 隨便開一個來抓columns
with open(path + '/' + file_list[0], 'r', encoding='utf-8') as f:
    tmp_data = f.read().split('\n')
columns = []
for i in range(len(tmp_data)):
    columns.append(tmp_data[i].split(':')[0])
columns = columns[:-1]
# print(columns)
# 比對資料，順便看所有欄位是否一樣
data = []
for file_name in file_list:
    with open(path + '/' + file_name, 'r', encoding='utf-8') as f:
        tmp_data = f.read().split('\n')
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
lambda s: s.split(': ')[-1]

def column_filter(s):
    output = s.split(': ')[-1]
    return output
for i in columns:
    df[i] = df[i].apply(column_filter)
# print(df)
df.to_csv('./try_104.csv', index=0, encoding='utf_8_sig')



