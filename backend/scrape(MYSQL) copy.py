from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import time

# 連接資料庫
con = mysql.connector.connect(
    user="root",
    password="12345678",
    host="localhost",
    database="restaurant",
    port=3305
)
print("連線成功")

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
            restaurant_data.append((name, image_url, href_element))
        except Exception as e:
            print(f"Error extracting data: {e}")
    return restaurant_data

# 自動滾動直到獲取100家餐廳資料
def get_100_restaurants():
    all_restaurant_data = set()
    while len(all_restaurant_data) < 100:
        scroll()  # 滾動頁面
        restaurant_data = get_restaurant_data()  # 獲取餐廳資料
        all_restaurant_data.update(restaurant_data)
        print(f"Found {len(all_restaurant_data)} restaurants so far.")
    
    return list(all_restaurant_data)[:100]  # 確保只返回 100 家餐廳資料

# 執行自動滾動直到獲取100家餐廳資料
restaurants = get_100_restaurants()
print(f"Total restaurants found: {len(restaurants)}")
print(restaurants)

cursor = con.cursor()

# 清空表中的現有數據
cursor.execute("TRUNCATE TABLE rest")
con.commit()

# 插入新的餐廳資料
insert_query = "INSERT INTO rest (rest_name, rest_image, rest_href) VALUES (%s, %s, %s)"
for restaurant in restaurants:
    cursor.execute(insert_query, restaurant)

con.commit()
print(f"Inserted {cursor.rowcount} rows into the database.")

driver.quit()
