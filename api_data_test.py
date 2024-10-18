import requests
import pandas as pd

test_url =
order_num_url = 'https://api.syf.com.tw/api/v_datav_01_01.php?act=orderAndInquiry&prop=syfgift&freq=week'
seven_oreder_cash_url = 'https://api.syf.com.tw/api/v_datav_01_01.php?act=orderAndInquiry&prop=syfgift&freq=month'
response_order = requests.get(order_num_url)
response_cash = requests.get(seven_oreder_cash_url)
test = requests.get(test_url)


if response_cash.status_code == 200:
    data = test.json()
    df = pd.DataFrame(data)
#    print(test.text)  # 查看伺服器返回的原始內容
    print(df)
else:
    print(f"Error:{response_cash.status_code}")