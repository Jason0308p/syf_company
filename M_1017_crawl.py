from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pygsheets
import pandas as pd

# 設定搜尋的頁數切片和起點
search_page = 2
num = 1

target_jscontroller = "SC7lYd"
target_url_part = "syf.tw"

def search_and_scroll(search_query):
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        total_position = 0  # 定義當前排名和總排名計數器
        syf_data = []
        sponsor_ad_count = 0
        current_page = 1
        found_any = False

        while current_page <= search_page:
            time.sleep(1)  # 加大等待時間

            # 記錄當前搜尋頁的 url
            current_page_url = driver.current_url

            # 紀錄搜尋頁出現贊助商廣告的數量
            ad_label = driver.find_elements(By.XPATH, ".//span[contains(text(),'贊助商廣告')]")
            sponsor_ad_count += len(ad_label)

            # 獲取當前頁面所有符合 jscontroller 的 div 元素
            elements = driver.find_elements(By.XPATH, f"//div[@jscontroller='{target_jscontroller}']")

            for index, element in enumerate(elements, start=1):
                total_position += 1
                try:
                    if target_url_part in element.text:
                        syf_url = element.find_element(By.XPATH, ".//cite").text
                        href_link = element.find_element(By.XPATH, ".//a[@jsname='UWckNb']").get_attribute("href")
                        print(f"目標網址出現在第 {total_position} 個搜尋結果 (第 {current_page} 頁, 第 {index} 個)")

                        syf_data.append({
                            'Google 搜尋網址': current_page_url,
                            'SYF網址': syf_url,
                            'href到達連結': href_link,
                            '廣告數量': sponsor_ad_count,
                            '到達頁數': current_page,
                            '排名': total_position
                        })
                        found_any = True

                except Exception as e:
                    print(f"Error: {e}")
                    continue

            current_page += 1
            try:
                next_button = driver.find_element(By.ID, "pnnext")
                next_button.click()
            except Exception as e:
                print(f"Error clicking next page: {e}")
                break

        return syf_data

    finally:
        driver.quit()

def batch_search(search_queries):
    results = []  # 用於存儲所有查詢的結果
    for index, query in enumerate(search_queries, start=1):
        print(f"\n----- 開始查詢第 {index} 個關鍵字: {query} -----\n")
        syf_data = search_and_scroll(query)

        if syf_data:
            results.extend(syf_data)  # 將每次查詢的結果添加到總結果中

    return results  # 返回包含子列表的列表，每個子列表表示一個查詢的結果

# Google Sheet 操作
url = "C:/Users/syf/Desktop/code/data0923-a22f23dd44ce.json"
sheet_url = "https://docs.google.com/spreadsheets/d/18H9Qh64jqWMRNnv_-tLj85mkUCYAYjulTHqiHX7zrdk/edit"

gc = pygsheets.authorize(service_file=url)
sheet_name = gc.open_by_url(sheet_url)
sheets = sheet_name.worksheets()

# 關鍵字數目
start_cell = 2
end_cell = 4
start = "A" + str(start_cell)
end = "A" + str(end_cell)

query_data = sheets[2].get_values(start, end)
queries = [row[0] for row in query_data]

if __name__ == "__main__":
    final_results = batch_search(queries)
    df = pd.DataFrame(final_results, columns=['Google 搜尋網址', 'SYF網址', 'href到達連結', '廣告數量', '到達頁數', '排名'])

    # 重要!!! 把dataframe資料為 nan 轉換成 None，因為google sheet 只讀得懂 None
    data_to_insert = df.values.tolist()

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    for number in range(len(data_to_insert)):
        data_to_insert[number] = [None if pd.isna(x) else x for x in data_to_insert[number]]
        sheets[2].update_row(start_cell + number, values=data_to_insert[number], col_offset=1)

    print("\n----- 最終結果 -----")
    print(df)
