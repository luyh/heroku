from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pickle

mobileEmulation = {'deviceName': 'iPhone X'}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)

driver = webdriver.Chrome(executable_path='/Users/Hebbelu/Downloads/chromedriver',\
                                           chrome_options=options)

driver.set_window_size(50,800)
driver.get('http://hpg.sqk2.cn/public/apprentice.php/passport/login.html')
# print(driver.capabilities)
# print(driver.command_executor._url)
# print(driver.session_id)
# print(driver.command_executor.keep_alive)

params = {}
params["session_id"] = driver.session_id
params["server_url"] = driver.command_executor._url

f = open("chrome/params.data", 'wb')
# 转储对象至文件
pickle.dump(params, f)
f.close()