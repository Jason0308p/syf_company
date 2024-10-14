# 這個程式碼目前有錯誤，因為讀取到有缺失值，而不是完整的直行資料


import pandas as pd

# 讀取txt檔案，將每一行作為一個列表元素
with open('data.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()

# 移除每行結尾的換行符號
data = [line.strip() for line in data]

# 定義欄位名稱
columns = ['沖帳日', '工單編號', '工單名稱', '業務名', '原訂單額', '修改', '已收累計',
           '其他減項名稱', '其他減項費用', '收款類別', '收款金額', '匯款資訊', '收款銀行', '收款日期']

# 每個記錄有14個欄位，將data按14個數據為一組進行分割
records = [data[i:i + len(columns)] for i in range(0, len(data), len(columns))]

# 創建DataFrame
df = pd.DataFrame(records, columns=columns)

# 查看結果
print(df)

# 將結果輸出為 Excel 或 CSV 文件
df.to_excel('output.xlsx', index=False)  # 匯出到 Excel
#df.to_csv('output.csv', index=False)     # 匯出到 CSV
