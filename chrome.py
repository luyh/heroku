from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time
import _thread


# 打印系统系统
systerm = sys.platform
print( '系统类型:', systerm )

mobileEmulation = {'deviceName': 'iPhone 4'}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)

def chrome():
    # 连接Chrome
    print( u'正在连接chrome浏览器...' )
    if systerm.startswith( 'darwin' ):

        driver = webdriver.Chrome(executable_path='/Users/Hebbelu/Downloads/chromedriver',\
                                           chrome_options=options)
    elif systerm.startswith( 'linux' ):
        driver = webdriver.Chrome(chrome_options=options)

    elif systerm.startswith('win32'):
        driver = webdriver.Chrome(executable_path='.\chromedriver.exe',chrome_options=options)

    time.sleep( 3 )
    print( u'已打开chrome浏览器，并成功连接' )

    return driver


def _refresh(driver, delay):
    while 1:
        driver.refresh()
        time.sleep( delay )

def start_refresh_thread(driver,delay=30):
    _thread.start_new_thread( _refresh, (driver, delay) )

def stop_reflash_thread(driver):
    pass

def new_window(driver):
    js = js='window.open();'
    driver.execute_script(js)



if __name__ == '__main__':
    driver = chrome()
    driver.set_window_size(500, 500)
    driver.get('http://www.baidu.com')
    time.sleep(5)
    start_refresh_thread(driver)
    time.sleep(5)
    driver.quit()