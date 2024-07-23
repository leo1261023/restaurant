import pandas as pd
import json

# 讀取 Excel 文件
excel_file_path = r'C:\Users\user\Desktop\restaurant\rest-rec\public\restaurants_data.xlsx'
df = pd.read_excel(excel_file_path)

# 將 DataFrame 轉換為 JSON 格式
json_data = df.to_json(orient='records', force_ascii=False, indent=2)

# 將 JSON 數據寫入文件
json_file_path = r'C:\Users\user\Desktop\restaurant\rest-rec\public\restaurants_data.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print('Excel 文件已成功轉換為 JSON 文件')
