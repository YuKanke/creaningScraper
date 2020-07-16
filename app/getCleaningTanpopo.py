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
    URL = 'http://www.cleaning-tanpopo.jp/company/shop_area01.html'

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
    sleep(10)
 
    areaList = d.find_elements_by_xpath("//ul[@class='shopBtns cf']/li/a")
    areaURLs = {}
    for area in areaList:
        areaURLs[area.text] = area.get_attribute("href")

    for areaName, areaURL in areaURLs.items():
        d.get(areaURL)
        sleep(10)
        print("■■■■■■■■■■■" + areaName + "■■■■■■■■■■■") 

        shopList = d.find_elements_by_xpath("//ul[@id='shopList']/li")
        for shop in shopList:
            shopName = shop.find_element_by_tag_name("h5").text
            shopInfo = shop.find_elements_by_tag_name("td")
            address = shopInfo[1].text.replace("\n","")
            eigyou = shopInfo[0].text.split("\n")[0]
            tel = shopInfo[3].text
            kyujitu = shopInfo[0].text.split("\n")[1]
            print(shopName + " / " + address + " / " + tel + " / " + eigyou + " / " + kyujitu)
            print("---------------------------")
            row = []
            row.append(shopName)
            row.append(address)
            row.append(tel)
            row.append(eigyou)
            row.append(kyujitu)

            rtn.append(row)

    d.quit()
    return rtn
if __name__ == '__main__':
    main()
