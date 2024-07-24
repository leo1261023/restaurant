from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup

# 設置 Chrome 選項
options = Options()
options.add_argument("--start-maximized")  # 最大化瀏覽器窗口
chrome_driver_path = r"C:\Users\user\scraping\chromedriver.exe"

# 創建 Chrome 驅動實例
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com/maps/place/%E5%AE%8B%E5%BB%9A%E8%8F%9C%E9%A4%A8/@25.0323521,121.5384209,14z/data=!4m12!1m2!2m1!1z5Y-w5YyX5L-h576p5Y2A5Lit5byP6aSQ5buz!3m8!1s0x3442abb95596bec3:0x1feb3e03f2edcf3d!8m2!3d25.0417878!4d121.5654718!9m1!1b1!15sChvlj7DljJfkv6HnvqnljYDkuK3lvI_ppJDlu7NaISIf5Y-w5YyXIOS_oee-qSDljYAg5Lit5byPIOmkkOW7s5IBEmNoaW5lc2VfcmVzdGF1cmFudJoBI0NoWkRTVWhOTUc5blMwVkpRMEZuU1VOTE9XRmZVVmxCRUFF4AEA!16s%2Fg%2F1tvrxdpt?authuser=0&entry=ttu")

# 定義展開評論的函數
def expand_comments():
    while True:
        try:
            # 找到所有未展開的評論按鈕
            more_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.w8nwRe.kyuRq[aria-expanded="false"]')
            if not more_buttons:
                break  # 如果沒有未展開的按鈕，則退出循環
            for button in more_buttons:
                button.click()  # 點擊按鈕展開評論
                time.sleep(2)  # 等待評論內容展開
        except Exception as e:
            print("Error expanding comments:", e)
            break

# 定義滾動並展開評論的函數
def scroll_and_expand(target_comment_count=15):
    collected_comments = []
    try:
        # 等待評論面板出現
        pane = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde'))
        )
        while len(collected_comments) < target_comment_count:
            # 滾動評論面板
            driver.execute_script("arguments[0].scrollBy(0, 1000);", pane)
            time.sleep(10)  # 等待滾動
            # 獲取當前頁面的評論
            comments = driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf.fontBodyMedium')
            for comment in comments:
                try:
                    # 找到並點擊展開評論按鈕
                    more_button = comment.find_element(By.CSS_SELECTOR, 'button.w8nwRe.kyuRq[aria-expanded="false"]')
                    more_button.click()
                    time.sleep(5)  # 等待評論展開
                except:
                    pass
                # 獲取評論文本
                comment_text = comment.find_element(By.CLASS_NAME, 'MyEned').text
                if comment_text not in collected_comments:
                    collected_comments.append(comment_text)  # 收集評論文本
                    if len(collected_comments) >= target_comment_count:
                        break
    except Exception as e:
        print("Error in scrolling and expanding comments:", e)
    return collected_comments

# 定義獲取餐廳評論的函數
def get_reviews_for_restaurant(restaurant_link, num_reviews=15):
    reviews = []
    try:
        restaurant_name = restaurant_link.get_attribute('aria-label')
        print(f"店名: {restaurant_name}")  # 調試信息

        restaurant_link.click()  # 點擊餐廳連結
        time.sleep(5)  # 等待頁面加載

        # 等待評論選項卡可點擊
        reviews_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="Gpq6kf fontTitleSmall" and text()="評論"]'))
        )
        reviews_tab.click()  # 點擊評論選項卡
        time.sleep(5)  # 等待評論加載

        # 滾動並展開評論
        scroll_and_expand(target_comment_count=num_reviews)

        # 使用 BeautifulSoup 解析頁面內容
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        elements = soup.find_all("div", {"class": "jftiEf fontBodyMedium"})

        for ele in elements:
            try:
                comment = ele.find("span", {"class": "wiI7pd"}).get_text()
            except:
                comment = ""
            try:
                guide = ele.find("div", {"class": "RfnDt"}).get_text()
            except:
                guide = ""
            try:
                recommand = ele.find("span", {"class": "pkWtMe"}).get_text()
            except:
                recommand = "0"
            try:
                star = ele.find("span", {"class": "kvMYJc"}).get("aria-label")
            except:
                star = ""
            try:
                # 檢查是否有圖片
                images = ele.find_all("button", {"class": "Tya61d"})
                has_image = "Yes" if images else "No"
            except:
                has_image = "No"

            reviews.append((restaurant_name, comment, star, guide, recommand, has_image))  # 收集評論信息

            if len(reviews) >= num_reviews:
                break

    except Exception as e:
        print("Error:", e)

    finally:
        driver.back()  # 返回上一頁
        time.sleep(5)

    return reviews

try:
    # 等待並獲取所有餐廳連結
    restaurant_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'hfpxzc'))
    )[:1]

    all_reviews = []
    for i, link in enumerate(restaurant_links):
        print(f"正在爬取第 {i+1} 家餐廳的評論")
        reviews = get_reviews_for_restaurant(link, num_reviews=15)
        all_reviews.extend(reviews)

    # 將結果存入Pandas DataFrame
    df = pd.DataFrame(all_reviews, columns=["店名", "評論", "評分", "在地嚮導", "是否推薦評論", "是否有圖片"])

    # 印出
    print(df)
    # df.to_csv("testt_new.csv", encoding="utf-8-sig", index=False)

except Exception as e:
    print("Error:", e)
finally:
    driver.quit() 