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
    URL = 'https://www.pony-cl.co.jp/shop/'

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
    #a = len(d.find_elements_by_xpath("/html/body[@id='shop']/div[@class='layoutWrapper']/section[@id='contents']/div[@class='layoutInner']/section[@class='search']/div[@class='pcOnly']/div[@class='capitalArea left' or @class='chukyoArea right']"))
    #print(a)
    areaList = d.find_elements_by_xpath("/html/body[@id='shop']/div[@class='layoutWrapper']/section[@id='contents']/div[@class='layoutInner']/section[@class='search']/div[@class='pcOnly']/div[@class='capitalArea left' or @class='chukyoArea right']/div[@class='areaList left' or @class='areaList right']/ul/li/a")
# areaList = d.find_element_by_class_name("search").find_element_by_class_name("pcOnly").find_elements_by_tag_name("a")
    areaURLs = {}
    for area in areaList:
        areaURLs[area.get_attribute("textContent")] = area.get_attribute("href")

    for areaName, areaURL in areaURLs.items():
        d.get(areaURL)
        print("■■■■■■■■■■■" + areaName + "■■■■■■■■■■■")
        sleep(10)
#        print(len(d.find_elements_by_xpath("/html/body[@id='shop']/div[@class='layoutWrapper']/section[@id='contents']/div[@class='layoutInner']")))
        shopList = d.find_elements_by_xpath("/html/body[@id='detail']/div[@class='layoutWrapper']/section[@id='contents']/div[@class='layoutInner']/div[@class='container detail']/div[@class='inner']/section[@class='section']")
        for shop in shopList:
            shopName = shop.find_element_by_tag_name("h2").text
            shopInfo = shop.find_element_by_class_name("dataTable")
            address = shopInfo.find_elements_by_tag_name("td")[0].text
            tel = shopInfo.find_elements_by_tag_name("td")[1].text
            eigyou = shopInfo.find_elements_by_tag_name("td")[2].text
            kyujitu = shopInfo.find_elements_by_tag_name("td")[3].text
            print(shopName + " / " + address + " / " + tel + " / " + eigyou + " / " + kyujitu)
            print("---------------------------")

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
