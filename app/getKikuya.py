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
    URL = 'https://www.kikuya-cl.co.jp/kmobile/shoplist/'

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

    shopList = d.find_elements_by_xpath("/html/body[@id='shoplist']/article/section[@class='section']/ul[@class='accordion']/li/ul/li/a")
    shopURLs = {}
    for shop in shopList:
        print(shop.find_element_by_class_name("name").get_attribute("textContent"))
        shopURLs[shop.find_element_by_class_name("name").get_attribute("textContent")] = shop.get_attribute("href")
        
    print(len(shopList))
    for shopName, shopURL in shopURLs.items():
        d.get(shopURL)
        sleep(10)
        print("■■■■■■■■■■■" + shopName + "■■■■■■■■■■■")

        shopName = d.find_element_by_class_name("shopname").text

        shopInfo = d.find_element_by_class_name("adr").text
        address = shopInfo.split("\n")[1]
        tel = d.find_element_by_class_name("contact-area").find_elements_by_tag_name("p")[2].text
        eigyou = shopInfo.split("\n")[2]
        kyujitu = shopInfo.split("\n")[3]
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
