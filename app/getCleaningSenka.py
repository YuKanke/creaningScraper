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
    URL = 'https://cleaningsenka.jp/pokesen/shop/xs=_M4xbDjF97YYe/'

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

    finishedCities = []   

 
    areaList = d.find_elements_by_xpath("/html/body/div[@id='wrapper']/div[@id='container']/div[@id='main']/div[@id='contents']/ul[@id='shop_index']/li/a")
    areaURLs = {}
    for area in areaList:
        areaURLs[area.text] = area.get_attribute("href")

    for areaName, areaURL in areaURLs.items():
        d.get(areaURL)
        sleep(10)
        print("■■■■■■■■■■■" + areaName + "■■■■■■■■■■■") 
        cityList = d.find_elements_by_xpath("/html/body/div[@id='wrapper']/div[@id='container']/div[@id='main']/div[@id='contents']/div[@id='area_index']/ul[@class='clearfix']/li/a")
        cityURLs = {}
        for city in cityList:
            cityURLs[city.text] = city.get_attribute("href")
        for cityName, cityURL in cityURLs.items():
            if not cityName in finishedCities:
                print("--------------" + cityName + "--------------")
                d.get(cityURL)
                sleep(10)
                shopList = d.find_elements_by_xpath("/html/body/div[@id='wrapper']/div[@id='isu_content']/div[@id='container']/div[@id='main']/div[@id='contents']/div[@id='shop_table']")
                for shop in shopList:
                    shopName = shop.find_element_by_tag_name("h4").text
                    shopInfo = shop.find_elements_by_tag_name("td")
                    address = shopInfo[0].text
                    eigyou = shopInfo[1].text
                    tel = shopInfo[2].text
                    kyujitu = shopInfo[3].text
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
