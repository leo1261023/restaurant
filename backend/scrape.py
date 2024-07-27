from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# 設置 Chrome 選項
options = Options()
options.add_argument("--start-maximized")  # 最大化瀏覽器窗口
chrome_driver_path = r"C:\Users\user\scraping\chromedriver.exe"
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com/maps/search/%E5%8F%B0%E5%8C%97%E9%A4%90%E5%BB%B3/@25.032502,121.5384209,14z/data=!3m1!4b1?authuser=0&entry=ttu")

def scroll_and_get_data():
    all_restaurant_data = []
    while len(all_restaurant_data) < 30:
        scroll_elements = driver.find_elements(By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde')
        if not scroll_elements:
            print("No scrollable elements found.")
            break
        
        for getscroll in scroll_elements:
            driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight", getscroll)
            time.sleep(2)  # 等待滾動

        restaurant_elements = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')
        for element in restaurant_elements:
            try:
                name_element = element.find_element(By.CSS_SELECTOR, 'a.hfpxzc')
                name = name_element.get_attribute('aria-label')
                image_element = element.find_element(By.CSS_SELECTOR, 'img')
                image_url = image_element.get_attribute('src')
                href_element = name_element.get_attribute('href')
                all_restaurant_data.append({
                    "name": name,
                    "image": image_url,
                    "href": href_element
                })
                if len(all_restaurant_data) >= 30:
                    break
            except Exception as e:
                print(f"Error extracting data: {e}")
        print(f"Found {len(all_restaurant_data)} restaurants so far.")
    
    return all_restaurant_data[:30]  # 確保只返回 30 家餐廳資料

# 執行滾動並獲取30家餐廳資料
restaurants = scroll_and_get_data()
print(f"Total restaurants found: {len(restaurants)}")
print(restaurants)

# 將資料儲存到本地 JSON 檔案中
with open(r'C:\Users\user\Desktop\restaurant\rest-rec\public\toprestaurants.json', 'w', encoding='utf-8') as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=4)
print("Data saved to public/restaurants.json")

driver.quit()
