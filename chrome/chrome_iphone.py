# -*- coding: utf-8 -*-

from selenium import webdriver

from time import sleep

mobileEmulation = {'deviceName': 'iPhone 4'}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)
driver = webdriver.Chrome(executable_path='/Users/Hebbelu/Downloads/chromedriver', chrome_options=options)

driver.set_window_size(10,800)
driver.get('http://hpg.sqk2.cn/public/apprentice.php/task/index.html')

sleep(15)

driver.close()