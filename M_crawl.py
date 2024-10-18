from openpyxl.styles.builtins import total
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pygsheets
import pandas as pd

# 設定每次搜尋2頁
search_page = 2
total_pages = 3  # 總共要搜尋的頁數
num = 1  # 選擇要使用的 sheet 工作表

# 搜尋並滾動
def search_and_scroll(search_query, start_page):
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(0.6)


        # 點擊跳轉到指定的起始頁
        if start_page > 1:
            page_link = driver.find_element(By.XPATH, f'//a[@aria-label="Page {start_page}"]')
            page_link.click()

        syf_data = []
        sponsor_ad_count = 0
        current_page = start_page
        max_pages = start_page + search_page - 1

        while current_page <= max_pages:
            time.sleep(0.6)

            current_page_url = driver.current_url
            ad_label = driver.find_elements(By.XPATH, ".//span[contains(text(),'贊助商廣告')]")
            sponsor_ad_count += len(ad_label)

            # 獲取含有 syf.tw 的搜尋結果
            url_elements = driver.find_elements(By.XPATH, ".//cite[@role='text' and contains(text(),  'syf.tw')]")
            for element in url_elements:
                syf_data.append({
                    'syf_url': element.text,
                    'page': current_page,
                    'google_search_page_url': current_page_url
                })

            # 滾動到頁面底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.6)

            # 下一頁
            try:
                next_button = driver.find_element(By.ID, "pnnext")
                next_button.click()
                current_page += 1
            except Exception as e:
                print(f"無法點擊下一頁: {e}")
                break

        return syf_data, sponsor_ad_count
    finally:
        driver.quit()

# 批量搜尋並整合數據
def batch_search(search_queries):
    results = []  # 存储所有查询的结果

    for query in search_queries:
        combined_syf_data = []  # 用來整合該次搜尋所有頁數的數據
        total_sponsor_ad_count = 0

        for start_page in range(1, total_pages + 1, search_page):
            print(f"查詢關鍵字: {query}, 頁數範圍: 第 {start_page} 到 {start_page + search_page - 1} 頁")
            syf_data, sponsor_ad_count = search_and_scroll(query, start_page)

            combined_syf_data.extend(syf_data)  # 整合該次兩頁的數據
            total_sponsor_ad_count += sponsor_ad_count  # 總廣告數累加

        # 如果整合結果中有 syf.tw 的網址
        if combined_syf_data:
            for entry in combined_syf_data:
                results.append([
                    entry['syf_url'],
                    total_sponsor_ad_count,  # 該次搜尋的總廣告數
                    entry['page'],
                    entry['google_search_page_url']
                ])
        else:
            # 沒有找到 syf.tw 結果時
            results.append([None, total_sponsor_ad_count, 999, None])

    return results

# Google Sheets 操作
url = "C:/Users/syf/Desktop/code/data0923-a22f23dd44ce.json"
sheet_url = "https://docs.google.com/spreadsheets/d/18H9Qh64jqWMRNnv_-tLj85mkUCYAYjulTHqiHX7zrdk/edit"

gc = pygsheets.authorize(service_file=url)
sheet_name = gc.open_by_url(sheet_url)
sheets = sheet_name.worksheets()

# 關鍵字數目
start_cell = 2
end_cell = 3
total_query = end_cell - start_cell + 1
query_data = sheets[1].get_values(f"A{start_cell}", f"A{end_cell}")
queries = [row[0] for row in query_data]

if __name__ == "__main__":
    final_results = batch_search(queries)
    df = pd.DataFrame(final_results, columns=['SYF網址', '廣告數量', '頁數', 'Google搜尋頁面URL'])

    data_to_insert = df.values.tolist()

    for number in range(len(data_to_insert)):
        data_to_insert[number] = [None if pd.isna(x) else x for x in data_to_insert[number]]
        sheets[1].update_row(start_cell + number, values=data_to_insert[number], col_offset=1)

    print("\n----- 最終結果 -----")
    print(df)
    print(f'查詢 {start_cell} 到{end_cell}，共 {total_query} 個關鍵字')
