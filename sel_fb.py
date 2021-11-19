from selenium.webdriver import Chrome
import time
import pyautogui
from bs4 import BeautifulSoup
import pandas as pd
# 設定exe檔位置
driver = Chrome("C:\\Users\\q1217\\Desktop\\AI大數據課程\\R 與 python 機器學習實務\\FB與IG爬蟲20210914課程\\chromedriver.exe")

# 設定要開啟的網頁
driver.get("https://mbasic.facebook.com/")
# 填寫帳號密碼
# 帳號
driver.find_element_by_id("m_login_email").send_keys("a60112222@yahoo.com")
# 密碼
driver.find_element_by_name("pass").send_keys("python123")
# 點擊登入
driver.find_element_by_name("login").click()
# 等待時間
time.sleep(2)
# 進入社團
driver.get("https://mbasic.facebook.com/groups/498729124625585")

# 模擬滑鼠滾動
for j in range(2):
    time.sleep(0.5)
    pyautogui.press('pgdn')
# 讀取網頁內容
soup = BeautifulSoup(driver.page_source)
#print(soup)
u = soup.find_all('a',class_='dd de')
print(u)
# 整理出每篇貼文的網址
u_count = len(u)
link_list = []
for i in range(u_count):
    url_str =u[i]["href"].split('?', 2)[0]
    print(url_str)
    link_list.append(str(url_str))
   
# 存成一個dataframe格式並將欄位命名為link
dataframe1 = pd.DataFrame({'link': link_list})
# 讀取長度
df_count = len(dataframe1.index)
for i in range(df_count):
    # 讀取每個連結
    url = dataframe1['link'][i]
    # 載入網頁
    driver.get(url)
    # 等待
    time.sleep(2)
    # 解析網頁
    soup = BeautifulSoup(driver.page_source)
    all_content = []
    # 尋找貼文內容
    find_date = soup.find_all('div', class_='bi bj')
    for e in find_date:
        # 尋找時間
        date = e.find('abbr').text
        #尋找內文
        try:
            content = e.find('div', class_='ca').text
            all_content.append(content)
        except:
            pass
        
    
    # 尋找回覆內容
    try:
        find_message = soup.find_all('div', class_="ee")
        all_message = []
        for w in find_message:
            message = w.text
            all_message.append(message)
        all_message = str(all_message)
    except:
            pass
    # 社團名稱
    source = 'pchome'
    # 每篇貼文的連結
    link = dataframe1['link'][i]
    # 製作dataframe
    dataframe2 = pd.DataFrame({'社團名稱': source, '日期': date, '發文內容': all_content, '回覆內容': all_message, '該文連結': link})
    # 存檔
    dataframe2.to_excel('C:\\Users\\q1217\\Desktop\\Topic\\T10\\data\\' + str(i) + '.xlsx', index=False,encoding="utf-8-sig")
# 合併資料
dfs = []
for j in range(df_count):
    dfs.append(pd.read_excel('C:\\Users\\q1217\\Desktop\\Topic\\T10\\data\\' + str(j) + '.xlsx'))
    df = pd.concat(dfs)
df.to_excel('C:\\Users\\q1217\\Desktop\\Topic\\T10\\data\\result.xlsx', index=False,encoding="utf-8-sig")