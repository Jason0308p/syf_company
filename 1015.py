from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pygsheets
import pandas as pd


# 設定搜尋的頁數切片和起點 (因為無法一次瀏覽10頁，因此以2頁進行切片，才不會被視為機器人)
# num 為 gs 中第幾個工作表，看要爬蟲搜尋1~10頁， num * search_page
search_page = 2
num = 1

def search_and_scroll(search_query):
    driver = webdriver.Chrome()
    # 初始化 chrome 瀏覽器，自動下載與電腦 chrome 兼容的最新版本 chrome driver
    # webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get("https://www.google.com")

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        #time.sleep(15)

        # 點擊第 3 頁
        # 因為要從第 3 頁開始紀錄搜尋數據
        third_page_link = driver.find_element(By.XPATH, '//a[@aria-label="Page 3"]')
        third_page_link.click()

        next_page_count = 0
        sponsor_ad_count = 0
        syf_data = []

        # 共搜尋 ? 頁
        while next_page_count < 2:
        #while next_page_count < 10:
            time.sleep(1)

            # 記錄當前搜尋頁的 url
            current_page_url = driver.current_url

            # 紀錄搜尋頁出現贊助商廣告的數量
            ad_label = driver.find_elements(By.XPATH, ".//span[contains(text(),'贊助商廣告')]")
            sponsor_ad_count += len(ad_label)

            # 找搜尋頁出現新站的字段: syf.tw
            url_elements = driver.find_elements(By.XPATH, ".//cite[@role='text' and contains(text(),  'syf.tw')]")

            # 紀錄: 搜尋到的新站到達網址、搜尋頁的網址、頁數
            for element in url_elements:
                syf_data.append({
                    'syf_url': element.text,
                    'page': next_page_count + 1,
                    'google_search_page_url': current_page_url
                })

            # 滾動
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.6)

            # 下一頁
            try:
                next_button = driver.find_element(By.ID, "pnnext")
                next_button.click()
                next_page_count += 1
            except Exception as e:
                break
        return syf_data,sponsor_ad_count,next_page_count+1
    finally:
        driver.quit()

def batch_search(search_queries):
    results = []  # 用于存储所有查询的结果


    for index, query in enumerate(search_queries, start=1):
        print(f"\n----- 开始查询第 {index} 个关键字: {query} -----\n")
        syf_data,sponsor_ad_count,page_count = search_and_scroll(query)

        found = False  # 确保每次循环开始时都初始化

        if syf_data:
            for entry in syf_data:
                if not found:  # 如果还没找到有效的 URL
                    results.append([  # 使用列表来存储每个查询的结果
                        entry['syf_url'],  # SYF网址
                        sponsor_ad_count,  # 广告数量
                        page_count,      # 页数
                        entry['google_search_page_url']  # Google 搜索页面 URL
                    ])
                    found = True  # 找到第一个有效的 SYF URL，标志位置为 True

        # 如果没有找到有效的 syf URL
        if not found:
            results.append([
                None,
                sponsor_ad_count,
                999,
                None
            ])

        if index >=50:
            break
    return results  # 返回包含子列表的列表，每个子列表表示一个查询的结果


# google sheet  操作
url = "C:/Users/syf/Desktop/code/data0923-a22f23dd44ce.json"
sheet_url = "https://docs.google.com/spreadsheets/d/18H9Qh64jqWMRNnv_-tLj85mkUCYAYjulTHqiHX7zrdk/edit"

gc = pygsheets.authorize(service_file=url)
sheet_name = gc.open_by_url(sheet_url)
sheets = sheet_name.worksheets()

#關鍵字數目
start_cell = 3
end_cell =  5
start = "A" + str(start_cell)
end  = "A" + str(end_cell)

query_data = sheets[0].get_values(start, end)
queries = [row[0] for row in query_data]

if __name__ == "__main__":
    final_results = batch_search(queries)
    df = pd.DataFrame(final_results, columns=['广告数量', 'SYF网址', '页数', 'Google 搜索页面 URL'])

    # 重要!!! 把dataframe資料為 nan 轉換成 None，因為google sheet 只讀得懂None
    # df = df.where(pd.notnull(df),None)
    # print("DataFrame before converting to list:")
    # print(df)

    data_with_headers = [df.columns.tolist()] + df.values.tolist()
    data_to_insert = df.values.tolist()

    pd.set_option('display.max_rows',None)
    pd.set_option('display.max_columns',None)

    # 這段 update方式很實用
    # update_row 第一個參數為index，為輸入的row number
    # col_offset 為跳過幾個col後再輸入資料
    for number in range(len(data_to_insert)):


        # 重要!!!
        # 再次確保倒入 google sheet 時沒有nan
        data_to_insert[number] = [None if pd.isna(x) else x for x in data_to_insert[number]]
        sheets[0].update_row(start_cell+number, values=data_to_insert[number],col_offset=1)

    print("\n----- 最終結果 -----")
    print(df)

