from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
import datetime
import csv
import myFunc

# 定数的なの
URL = 'http://www.hakuyosha.co.jp/cleaning/shop/result/'
#URLs = ['http://concafenavi.com/area/hokkaido/']
googleDriveFolderId = "1nLocyxN40simk5Ud34s8-LIkmtmNJ2Fs"


chrome_path = '/usr/bin/chromium-browser'
chromedriver_path = '/usr/lib/chromium/chromedriver'
o = Options()
o.binary_location = '/usr/bin/chromium-browser'
o.add_argument('--headless')
o.add_argument('--disable-gpu')
o.add_argument('--no-sandbox')
o.add_argument('--window-size=720x360')

"""
Sample test
"""
#d = webdriver.Chrome(chromedriver_path, options=o)
#d.get('https://www.google.com')
#print(d.title)
#d.quit()

"""
Use the Chrome DriverService.
https://chromedriver.chromium.org/getting-started
"""
s = Service(executable_path=chromedriver_path)
s.start()
d = webdriver.Remote(
    s.service_url,
    desired_capabilities=o.to_capabilities()
)
#d.implicitly_wait(100)

d.get(URL)
#print(d.title)
sleep(10)
areaList = d.find_elements_by_xpath("/html/body[@id='shop']/div[@id='content']/div[@id='contentWrapper']/div[@id='contentLeft']/dl[@id='sideNavi']/dd/ul/li/a")
areaURLs = {}
for area in areaList:
    areaURLs[area.text] = area.get_attribute("href")

for areaName, areaURL in areaURLs.items():
    d.get(areaURL)
    print("■■■■■■■■■■■" + areaName + "■■■■■■■■■■■")
    while True: #下で判定してる
        sleep(10)
        shopList = d.find_elements_by_xpath("/html/body[@id='shop']/div[@id='content']/div[@id='contentWrapper']/div[@id='contentRight']/div[@class='contentBlock1']")
        for shop in shopList:
            shopName = shop.find_element_by_tag_name("h3").text
            shopInfo = shop.find_element_by_class_name("contentBlockBody").find_element_by_class_name("shopDetail")
            address = shopInfo.find_elements_by_tag_name("dd")[0].text
            tel = shopInfo.find_elements_by_tag_name("dd")[1].text
            eigyou = shopInfo.find_elements_by_tag_name("dd")[2].text
            kyujitu = shopInfo.find_elements_by_tag_name("dd")[3].text
            print(shopName + " / " + address + " / " + tel + " / " + eigyou + " / " + kyujitu)
            print("---------------------------")
        # ループ判定
        if d.find_elements_by_class_name("next"):
            nextURL = d.find_element_by_class_name("next").find_element_by_tag_name("a").get_attribute("href")
            print(nextURL)
            d.get(nextURL)
        else:
            break
d.quit()
