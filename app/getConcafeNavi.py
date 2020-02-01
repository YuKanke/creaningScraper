from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
import datetime
import csv
import myFunc

# 定数的なの
URLs = ['http://concafenavi.com/area/tokyo/','http://concafenavi.com/area/osaka/,http://concafenavi.com/area/chiba/','http://concafenavi.com/area/aich','http://concafenavi.com/area/fukuoka','http://concafenavi.com/kanagawa','http://concafenavi.com/area/saitama','http://concafenavi.com/area/tochigi','http://concafenavi.com/area/gumma']
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


Lists = {}

for URL in URLs:
    d.get(URL)
    #print(d.title)
    sleep(3)
    for shop in d.find_elements_by_class_name("archiveItem"):
        shopName = shop.find_element_by_class_name("hc")
        print(shopName.text + "⑳" + shopName.get_attribute("href"))
        Lists[shopName.text] = shopName.get_attribute("href")


print("■■■■■■■■■■■■■■■■■■■■■■■■■")

with open('./getConcafeNavi' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for name,URL in Lists.items():
        output = ""
        print(name + "-------"  + URL)
        d.get(URL)
        sleep(7)
        job_tables = d.find_elements_by_tag_name("table")
        output = name + "," + URL
        
        outList = []
        #try:
        #    outList.append(d.find_elements_by_class_name("mb20")[1].text)
        #except:
        #    outList.append(d.find_element_by_class_name("mb20").text)
        outList.append(name)
        outList.append(URL)
        for table in job_tables:
            for val in table.find_elements_by_tag_name("td"):
                outList.append(val.text)
        
        #1/28追加 サムネ画像を取得
        try: 
            if not d.find_elements_by_xpath("/html/body[@class='t-light']/div[@class='l-wrapper']/main[@class='l-main']/section[@class='content content-page']/div[@class='mb20 mt40']/img") == []:
                imageURL = d.find_element_by_xpath("/html/body[@class='t-light']/div[@class='l-wrapper']/main[@class='l-main']/section[@class='content content-page']/div[@class='mb20 mt40']/img").get_attribute("src")
                imageName = "images/" + name + ".png"
                myFunc.downloadFile(imageURL, imageName)
                imageID = myFunc.uploadFile(imageName,googleDriveFolderId)
                myFunc.removeFile(imageName)

                outList.append(imageURL)
                outList.append(imageName)
                outList.append(imageID)
            else:
                print("サムネ画像がページに存在しませんでした。")
        except:
            import traceback
            print(traceback.print_exc())

        writer.writerow(outList)
d.quit()
