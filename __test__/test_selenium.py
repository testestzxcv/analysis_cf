import time
from selenium import webdriver

wd = webdriver.Chrome('D:/bigdata/chromedriver/chromedriver.exe')
wd.get('http://www.google.com')

time.sleep(5)   # 5초 일시정지
html = wd.page_source
print(html)

wd.quit()   # 종료