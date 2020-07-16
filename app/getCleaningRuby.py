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
    URL = 'https://www.rby.jp/shop/'

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


 
    areaList = d.find_elements_by_class_name("prefectural-group__item--pc")
    areaURLs = {}
    for area in areaList:
        areaURLs[area.find_element_by_class_name("owl-img-roll").get_attribute("alt")] = area.find_element_by_tag_name("a").get_attribute("href")
        print(area.find_element_by_class_name("owl-img-roll").get_attribute("alt") + " "+ area.find_element_by_tag_name("a").get_attribute("href"))
    for areaName, areaURL in areaURLs.items():
        d.get(areaURL)
        sleep(10)
        print("■■■■■■■■■■■" + areaName + "■■■■■■■■■■■") 
        cityList = d.find_elements_by_class_name("prefectural-name")
        cityURLs = {}
        for city in cityList:
            cityURLs[city.find_element_by_tag_name("a").get_attribute("textContent")] = city.find_element_by_tag_name("a").get_attribute("href")
            print(city.find_element_by_tag_name("a").get_attribute("textContent") + city.find_element_by_tag_name("a").get_attribute("href"))
        for cityName, cityURL in cityURLs.items():
            print("--------------" + cityName + "--------------")
            d.get(cityURL)
            sleep(10)
            shopList = d.find_elements_by_class_name("shop-name")
            shopURLs = {}
            for shop in shopList:
                shopURLs[shop.find_element_by_tag_name("a").get_attribute("textContent")] = shop.find_element_by_tag_name("a").get_attribute("href")
            for shopName, shopURL in shopURLs.items():
                d.get(shopURL)
                sleep(10)
                shopInfo = d.find_elements_by_class_name("about-shop-table__td")
                address = shopInfo[0].text
                eigyou = shopInfo[2].text
                tel = shopInfo[1].text
                kyujitu = shopInfo[4].text
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
