# -*- coding: utf-8 -*

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from ulity.china_time import ChinaTime
import time,datetime
import sys,os


print(sys.platform)
print('Chrome opening...')
if sys.platform.startswith('win32'):
    driver = webdriver.Chrome(executable_path='.\chromedriver.exe')
elif sys.platform.startswith('linux'):
    driver = webdriver.Chrome()
elif sys.platform.startswith('darwin'):
    driver = webdriver.Chrome()
else:
    print('不支持此操作系统')

print(u'已打开chrome浏览器，并成功连接')

print('打开网页...')
driver.get("http://zhuankeban.com/jsp/Mobile/apprentice/ApprenticeLogin.jsp")
print(driver.title)

print('输入用户名及密码...')
input_user = driver.find_element_by_id('user_account')
input_user.clear()
username = os.getenv('HPG_USER')
print(username)
exit()
input_user.send_keys(username)

password = driver.find_element_by_id('user_password')
password.clear()
userpass = os.getenv('HPG_PASS')
password.send_keys(userpass)

print('点击登陆...')
sighinButton = driver.find_element_by_id('Signin')
sighinButton.click()
time.sleep(5)

print('切换我要买页面...')
toBuy = driver.find_element_by_link_text('我要买')
toBuy.click()
time.sleep(5)

now = ChinaTime()
while(1):
        now.getChinaTime()
        if (now.second ==15):
            print( now, '每分钟的第15s刷新页面' )
            driver.refresh()

        if(now.minute == 00 or now.minute == 30):
            print( now ,'到0分或30分，开始抢单！！！' )
            time.sleep(1)
            try:
                myBuy = driver.find_element_by_id("queue-up-task")
                ActionChains(driver).click(myBuy).perform()
            except:
                pass
            time.sleep(60)

        time.sleep(1)