from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import json

# 設置 Chrome 選項
options = Options()
chrome_driver_path = r"C:\Users\user\scraping\chromedriver.exe"
driver = webdriver.Chrome(options=options)

# 設置地區和菜系列表
areas = ["中正區", "大同區", "中山區", "松山區", "大安區", "萬華區", "信義區", "士林區", "北投區", "內湖區", "南港區", "文山區"]
cuisines = ["中式", "日式", "美式", "墨西哥菜", "泰式", "韓式", "印度菜", "法式", "越南菜", "地中海料理", "素食", "海鮮"]

def scroll_down():
    """
    模擬滾動特定元素，以加載更多的內容。
    """
    SCROLL_PAUSE_TIME = 2  # 滾動後的等待時間
    scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')  # 查找特定的滾動元素
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)  # 頁面初始高度

    while True:
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)  # 滾動元素到底部
        time.sleep(SCROLL_PAUSE_TIME)  # 等待頁面加載
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)  # 滾動後頁面高度
        if new_height == last_height:  # 如果高度不變，說明已經滾動到底部
            break
        last_height = new_height  # 更新最後的高度

def get_restaurant_data():
    """
    從加載的頁面中提取餐廳數據。
    """
    restaurant_data = []
    restaurant_elements = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')  # 找到所有餐廳元素

    for element in restaurant_elements:
        try:
            name = element.find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('aria-label')  # 餐廳名稱
            try:
                image = element.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')  # 餐廳圖片
            except:
                image = None  # 如果找不到圖片元素，設置為 None
            href = element.find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('href')  # 餐廳鏈接
            restaurant_data.append({
                'name': name,
                'image': image,
                'href': href
            })
        except Exception as e:
            print(f"Error extracting data: {e}")
    return restaurant_data

def scrape_restaurants(query):
    """
    爬取特定查詢條件的餐廳數據，直到至少找到30家餐廳。
    """
    all_data = []
    while len(all_data) < 100:
        url = f"https://www.google.com/maps/search/台北+{query}+餐廳"
        driver.get(url)
        time.sleep(10)  # 等待頁面加載
        scroll_down()  # 滾動頁面以加載更多餐廳
        
        new_data = get_restaurant_data()
        if not new_data:
            break
        all_data.extend(new_data)
        
        # 確保不超過30家餐廳
        if len(all_data) > 100:
            all_data = all_data[:100]
            break
    
    print(f"Found {len(all_data)} restaurants for {query}")
    
    return all_data[:50]

all_restaurants = []

# 爬取各地區的餐廳資料
for area in areas:
    data = scrape_restaurants(area)
    for restaurant in data:
        restaurant['category'] = 'area'  # 添加分類標籤
        restaurant['query'] = area  # 添加查詢條件標籤
    all_restaurants.extend(data)  # 將結果添加到總列表

# 爬取各菜系的餐廳資料
for cuisine in cuisines:
    data = scrape_restaurants(cuisine)
    for restaurant in data:
        restaurant['category'] = 'cuisine'  # 添加分類標籤
        restaurant['query'] = cuisine  # 添加查詢條件標籤
    all_restaurants.extend(data)  # 將結果添加到總列表

# 將數據保存為 JSON 文件
output_path = r'C:\Users\user\Desktop\restaurant\rest-rec\public\restaurants_data.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_restaurants, f, ensure_ascii=False, indent=4)

print(f"Saved all restaurant data to {output_path}")

driver.quit()
