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
    URLs = { \
        'https://www.white-ex.co.jp/shop/?pre=hokkaido' \
        ,'https://www.white-ex.co.jp/shop/?pre=aomori' \
        ,'https://www.white-ex.co.jp/shop/?pre=iwate' \
        ,'https://www.white-ex.co.jp/shop/?pre=miyagi' \
        ,'https://www.white-ex.co.jp/shop/?pre=akita' \
        ,'https://www.white-ex.co.jp/shop/?pre=yamagata' \
        ,'https://www.white-ex.co.jp/shop/?pre=fukushima' \
        ,'https://www.white-ex.co.jp/shop/?pre=ibaraki' \
        ,'https://www.white-ex.co.jp/shop/?pre=tochigi' \
        ,'https://www.white-ex.co.jp/shop/?pre=gunma' \
        ,'https://www.white-ex.co.jp/shop/?pre=saitama' \
        ,'https://www.white-ex.co.jp/shop/?pre=chiba' \
        ,'https://www.white-ex.co.jp/shop/?pre=tokyo' \
        ,'https://www.white-ex.co.jp/shop/?pre=kanagawa' \
        ,'https://www.white-ex.co.jp/shop/?pre=niigata' \
        ,'https://www.white-ex.co.jp/shop/?pre=toyama' \
        ,'https://www.white-ex.co.jp/shop/?pre=ishikawa' \
        ,'https://www.white-ex.co.jp/shop/?pre=fukui' \
        ,'https://www.white-ex.co.jp/shop/?pre=yamanashi' \
        ,'https://www.white-ex.co.jp/shop/?pre=nagano' \
        ,'https://www.white-ex.co.jp/shop/?pre=gifu' \
        ,'https://www.white-ex.co.jp/shop/?pre=shizuoka' \
        ,'https://www.white-ex.co.jp/shop/?pre=aichi' \
        ,'https://www.white-ex.co.jp/shop/?pre=mie' \
        ,'https://www.white-ex.co.jp/shop/?pre=shiga' \
        ,'https://www.white-ex.co.jp/shop/?pre=kyoto' \
        ,'https://www.white-ex.co.jp/shop/?pre=osaka' \
        ,'https://www.white-ex.co.jp/shop/?pre=hyogo' \
        ,'https://www.white-ex.co.jp/shop/?pre=nara' \
        ,'https://www.white-ex.co.jp/shop/?pre=wakayama' \
        ,'https://www.white-ex.co.jp/shop/?pre=tottori' \
        ,'https://www.white-ex.co.jp/shop/?pre=shimane' \
        ,'https://www.white-ex.co.jp/shop/?pre=okayama' \
        ,'https://www.white-ex.co.jp/shop/?pre=hiroshima' \
        ,'https://www.white-ex.co.jp/shop/?pre=yamaguchi' \
        ,'https://www.white-ex.co.jp/shop/?pre=tokushima' \
        ,'https://www.white-ex.co.jp/shop/?pre=kagawa' \
        ,'https://www.white-ex.co.jp/shop/?pre=ehime' \
        ,'https://www.white-ex.co.jp/shop/?pre=kochi' \
        ,'https://www.white-ex.co.jp/shop/?pre=fukuoka' \
        ,'https://www.white-ex.co.jp/shop/?pre=saga' \
        ,'https://www.white-ex.co.jp/shop/?pre=nagasaki' \
        ,'https://www.white-ex.co.jp/shop/?pre=kumamoto' \
        ,'https://www.white-ex.co.jp/shop/?pre=oita' \
        ,'https://www.white-ex.co.jp/shop/?pre=miyazaki' \
        ,'https://www.white-ex.co.jp/shop/?pre=kagoshima' \
        ,'https://www.white-ex.co.jp/shop/?pre=okinawa' \
    }


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

    for URL in URLs:
        shopURLs = {}
        d.get(URL)
        print(URL.replace("https://www.white-ex.co.jp/shop/?pre=",""))
        sleep(10)
        pageCount = 2
        while True:
            shopList = d.find_elements_by_xpath("//table[@id='shop-table-result']/tbody/tr")
            if shopList:
                for shop in shopList:
                    shopURLs[shop.find_element_by_tag_name("td").text] = shop.get_attribute("data-location-href")
                d.get(URL + "&list=" + str(pageCount))
                sleep(15)
                pageCount = pageCount + 1
            else:
                print(pageCount)
                break

        print(len(shopURLs))
        for shopName, shopURL in shopURLs.items():
            d.get(shopURL)
            sleep(10)

            shopInfo = d.find_elements_by_xpath("//table[@class='p-table  p-table--shop']//tr")
            address = ""
            tel = ""
            eigyou = ""
            kyujitu = ""
            for i in range(len(shopInfo)):
                if shopInfo[i].find_element_by_tag_name("th").text == "住所":
                    address = shopInfo[i].find_element_by_tag_name("td").text.replace("\n", " ")
                elif shopInfo[i].find_element_by_tag_name("th").text == "電話番号":
                    tel = shopInfo[i].find_element_by_tag_name("td").text
                elif shopInfo[i].find_element_by_tag_name("th").text == "営業時間":
                    eigyou = shopInfo[i].find_element_by_tag_name("td").text
                elif shopInfo[i].find_element_by_tag_name("th").text == "定休日":
                    kyujitu = shopInfo[i].find_element_by_tag_name("td").text

            if tel == "":
                tel = "情報なし"
            if eigyou == "":
                eigyou = "情報なし"
            if kyujitu == "":
                kyujitu = "情報なし"

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
