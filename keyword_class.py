import pygsheets
import pandas as pd
import re

url = "C:/Users/syf/Desktop/code/data0923-a22f23dd44ce.json"
sheet_url = "https://docs.google.com/spreadsheets/d/18H9Qh64jqWMRNnv_-tLj85mkUCYAYjulTHqiHX7zrdk/edit"
gc = pygsheets.authorize(service_file=url)
sheet_location = gc.open_by_url(sheet_url)
sheets = sheet_location.worksheets()



# 从 Google Sheets 获取数据
data_df = sheets[0].get_values("A1","B1564")
data_df2 = sheets[7].get_all_values()
#
 # 创建 DataFrame，第一行作为列名
df = pd.DataFrame(data_df[1:], columns=data_df[0])  # data_df[0] 为列名
df2 = pd.DataFrame(data_df2[1:], columns=data_df2[0])  # 同理


# 這段是資料欄位中的【對應】
# # 重置索引
# df.reset_index(drop=True, inplace=True)
# df2.reset_index(drop=True, inplace=True)
#
# # 去除列名中的前后空格
# df.columns = df.columns.astype(str).str.strip()
# df2.columns = df2.columns.astype(str).str.strip()
#
# # 打印 df2 的列名以确认
# print("df2 的列名：", df2.columns)
#
# # 确保 '舊分類' 和 '關鍵字' 列存在
# if '舊分類' not in df2.columns or 'OA關鍵字' not in df2.columns:
#     print("Error: '舊分類' 或 'OA關鍵字' 列不存在于 df2 中！")
# else:
#     # 定义分类查找函数
#     def find_classification(keyword, df2):
#         for _, row in df2.iterrows():
#             if keyword in row['OA關鍵字']:  # 使用 df2 中的正确定义的列
#                 return row['舊分類']  # 确保此列存在
#         return ''
#
#     # 应用匹配函数
#     df['新分類'] = df['搜尋關鍵字'].apply(lambda x: find_classification(x, df2))
#
#     # 插入新列到 Google Sheets 中
#     sheets[0].insert_cols(col=1, number=1, values=df['新分類'].values.tolist())


# 這段程式是將中文字去除
def remove_chinese(text):
    if re.fullmatch(r'[\u4e00-\u9fff]+', text):
        return '無'
    else:
        return re.sub(r'[\u4e00-\u9fff]+', '', text)

update_data = df['分類'].apply(remove_chinese).values

update_data = [[item] for item in update_data]
print(update_data)

sheets[0].update_values('B2:B1564', update_data)