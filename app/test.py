from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep

chrome_path = '/usr/bin/chromium-browser'
chromedriver_path = '/usr/lib/chromium/chromedriver'
o = Options()
o.binary_location = '/usr/bin/chromium-browser'
o.add_argument('--headless')
o.add_argument('--disable-gpu')
o.add_argument('--no-sandbox')
o.add_argument('--window-size=1200x600')

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

URLs = ['https://caferun.jp/shoplist/akihabara/','https://caferun.jp/shoplist/tokyo/','https://caferun.jp/shoplist/kanto/','https://caferun.jp/shoplist/osaka/','https://caferun.jp/shoplist/nagoya/','https://caferun.jp/shoplist/else/']

Lists = {}

for URL in URLs:
    d.get(URL)
    print(d.title)
    whileFlg=True
    while whileFlg:
        for shopName in d.find_elements_by_class_name("shop_name"):
            print(shopName.text + shopName.get_attribute("href"))
            Lists[shopName.text] = shopName.get_attribute("href")
            
        if not d.find_elements_by_class_name("next"):
            whileFlg=False
        else:
            d.find_element_by_class_name("next").find_element_by_tag_name("a").click()
            sleep(3)
    
#for Area in d.find_elements_by_class_name("f-found_link"):
#    print(Area.find_elements_by_tag_name("a").get_attribute('href'))
#    Area.click()
#    sleep(3)
#    for Shop in d.find_elements_by_class_name("free_shop"):
#        print(Shop.find_elements_by_class_name("shop_name ellipsis"))

d.quit()
