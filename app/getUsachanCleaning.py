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
    URL = 'https://www.usachan-shop.jp/search?pref_cd=&keyword=&factory_id=&p=1'

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

    while True: #下で判定してる
        d.get(URL)
        sleep(10)
        shopList = d.find_elements_by_xpath("//ul[@class='shop_list']/li")
        print(len(shopList))
        for shop in shopList:

            shopName = shop.find_element_by_tag_name("h3").text
            shopInfo = shop.find_element_by_class_name("txt").text.split("\n")
            address = shopInfo[0]
            tel = shopInfo[1].replace("TEL：","")
            eigyou = shopInfo[2].split(" 　")[0].replace("営業時間：","")
            kyujitu = shopInfo[2].split(" 　")[1].replace("定休日：","")
            print(shopName + " / " + address + " / " + tel + " / " + eigyou + " / " + kyujitu)
            print("---------------------------")

            row = []
            row.append(shopName)
            row.append(address)
            row.append(eigyou)
            row.append(tel)
            row.append(kyujitu)

            rtn.append(row)
        # ループ判定
        if d.find_elements_by_xpath("//a[@rel='next']"):
            URL = d.find_element_by_xpath("//div[@class='wp-pagenavi']/a[@rel='next']").get_attribute("href")
            print(URL)
        else:
            break
    d.quit()

    return rtn

if __name__ == '__main__':
    main()
