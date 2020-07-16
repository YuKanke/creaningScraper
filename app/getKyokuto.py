from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
import datetime
import csv
#import myFunc

def main():
    rtn = []
    # 定数的なの
    URL = 'https://k-cleaning.jp/shop-list/?pref=*'

    chrome_path = '/usr/bin/chromium-browser'
    chromedriver_path = '/usr/lib/chromium/chromedriver'
    o = Options()
    o.binary_location = '/usr/bin/chromium-browser'
    o.add_argument('--headless')
    o.add_argument('--disable-gpu')
    o.add_argument('--no-sandbox')
    o.add_argument('--window-size=720x360')

    s = Service(executable_path=chromedriver_path)
    s.start()
    d = webdriver.Remote(
        s.service_url,
        desired_capabilities=o.to_capabilities()
    )

    d.get(URL)
    sleep(15)

    shopList = d.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    shopURLs = {}
    for shop in shopList:
        shopName = shop.find_elements_by_tag_name("td")[1].text
        address = shop.find_elements_by_tag_name("td")[3].text.split("\n")[0]
        tel = shop.find_elements_by_tag_name("td")[3].text.split("\n")[1].replace("TEL.","")
        eigyou = "情報なし"
        kyujitu = "情報なし"
        print(shopName + " / " + address + " / " + tel + " / " + eigyou + " / " + kyujitu)

        row = []
        row.append(shopName)
        row.append(address)
        row.append(eigyou)
        row.append(tel)
        row.append(kyujitu)

        rtn.append(row)

    d.quit()

    return rtn

if __name__ == '__main__':
    main()
