from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time
import _thread

def _refresh(driver, delay):
    while 1:
        driver.refresh()
        time.sleep( delay )

def start_refresh_thread(driver,delay=30):
    _thread.start_new_thread( _refresh, (driver, delay) )

def stop_reflash_thread(driver):
    pass

    js = js='window.open();'
    driver.execute_script(js)
