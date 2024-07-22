from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import os


# 設置 Chrome 選項
options = Options()
options.add_argument("--start-maximized")  # 最大化瀏覽器窗口
chrome_driver_path = r"C:\Users\user\scraping\chromedriver.exe"
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com/maps/search/%E5%8F%B0%E5%8C%97%E9%A4%90%E5%BB%B3/@25.032502,121.5384209,14z/data=!3m1!4b1?authuser=0&entry=ttu")

def scroll():
    # 嘗試獲取所有可能的滾動元素
    scroll_elements = driver.find_elements(By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde')
    
    if not scroll_elements:
        print("No scrollable elements found.")
        return
    
    for getscroll in scroll_elements:
        initial_scroll_height = driver.execute_script("return arguments[0].scrollHeight", getscroll)      
        # 滾動
        for i in range(10):  # 滾動 10 次
            driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight", getscroll)
            time.sleep(2)  # 等待滾動

# 定義獲取餐廳資料的函數
def get_restaurant_data():
    # 等待餐廳元素出現
    restaurant_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Nv2PK'))
    )
    restaurant_data = []
    for element in restaurant_elements:
        try:
            name_element = element.find_element(By.CSS_SELECTOR, 'a.hfpxzc')
            name = name_element.get_attribute('aria-label')
            image_element = element.find_element(By.CSS_SELECTOR, 'img')
            image_url = image_element.get_attribute('src')
            href_element = name_element.get_attribute('href')
            restaurant_data.append({
                "name": name,
                "image": image_url,
                "href": href_element
            })
        except Exception as e:
            print(f"Error extracting data: {e}")
    return restaurant_data

# 自動滾動直到獲取30家餐廳資料
def get_30_restaurants():
    all_restaurant_data = []
    while len(all_restaurant_data) < 30:
        scroll()  # 滾動頁面
        restaurant_data = get_restaurant_data()  # 獲取餐廳資料
        all_restaurant_data.extend(restaurant_data)
        print(f"Found {len(all_restaurant_data)} restaurants so far.")
    
    return all_restaurant_data[:30]  # 確保只返回 30 家餐廳資料

# 執行自動滾動直到獲取30家餐廳資料
restaurants = get_30_restaurants()
print(f"Total restaurants found: {len(restaurants)}")
print(restaurants)



# 將資料儲存到本地 JSON 檔案中
with open(r'C:\Users\user\Desktop\restaurant\rest-rec\public\toprestaurants.json','w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=4)
print("Data saved to public/restaurants.json")

driver.quit()
