from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
mobileEmulation = {'deviceName': 'iPhone 4'}
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# driver就是当前浏览器窗口
driver = webdriver.Chrome(executable_path='/Users/Hebbelu/Downloads/chromedriver',chrome_options=chrome_options)

driver.get('http://www.qq.com')