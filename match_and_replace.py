import pandas as pd



path = r'C:\Users\syf\Desktop\test.xlsx'
df = pd.read_excel(path, sheet_name=0)

def match_and_replace(df):
    # 定義一個替換函數
    def get_prefix(a):
        # 找到與當前 '分類' 對應的 B4 核心編碼名稱
        # 使用 na=False 來忽略 NaN 值，na=False：
        # 在 str.contains 方法中添加 na=False
        # 這樣如果 B4核心編碼名稱 中有 NaN 值
        # 這些行就會被自動忽略，不會導致錯誤。
        match = df[df['B4核心編碼名稱'].str.contains(a.split('-')[0], na=False)]
        if not match.empty:
            return match['B4核心編碼名稱'].values[0]  # 返回第一個匹配的值
        return a  # 如果沒有匹配，返回原值

    # 對 '分類' 欄位應用替換函數
    df['分類'] = df['分類'].apply(get_prefix)
    return df

df = match_and_replace(df)
print(df)
