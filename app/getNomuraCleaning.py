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
    URL = 'https://nc-nomura.com/shop/list.php?pref=0&shikusyouson=&keywords=&lat=&lng=&smt=%E6%A4%9C%E7%B4%A2'

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

    shopList = d.find_elements_by_xpath("/html/body[@id='list']/article[@id='contents']/div[@id='main']/section[@class='block'][1]/div[@class='box']/div[@class='listWrap w90']")
    shopURLs = {}
    for shop in shopList:
        tmp = shop.find_element_by_class_name("name").find_element_by_tag_name("a")
        print(tmp.text + tmp.get_attribute("href"))
        shopURLs[tmp.text] = tmp.get_attribute("href")
        
    for shopName, shopURL in shopURLs.items():
        d.get(shopURL)
        sleep(10)
        print("■■■■■■■■■■■" + shopName + "■■■■■■■■■■■")

        address = d.find_element_by_xpath("/html/body[@id='more']/article[@id='contents']/div[@id='main']/section[@class='block']/div[@class='box']/div[@class='w90']").text
        tel = d.find_element_by_xpath("/html/body[@id='more']/article[@id='contents']/div[@id='main']/section[@class='block']/div[@class='box']/p[@class='btnPink btnClr w90']/a").text
        eigyou = d.find_element_by_xpath("/html[@class=' responsejs ']/body[@id='more']/article[@id='contents']/div[@id='main']/section[@class='block']/div[@id='tab02']/div[@class='boxWrap']/div[@class='box']/div[@class='w90'][1]").text + "\n" + \
        d.find_element_by_xpath("/html[@class=' responsejs ']/body[@id='more']/article[@id='contents']/div[@id='main']/section[@class='block']/div[@id='tab02']/div[@class='boxWrap']/div[@class='box']/div[@class='w90'][2]").text
        kyujitu = d.find_element_by_xpath("/html/body[@id='more']/article[@id='contents']/div[@id='main']/section[@class='block']/div[@id='tab02']/div[@class='boxWrap']/div[@class='box'][2]/div[@class='w90']").text
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
