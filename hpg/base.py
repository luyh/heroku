from selenium import webdriver
import time

class BASE(object):
    def __init__(self):
        self.login_url = None
        self.toBuy_url = None
        self.status = None
        self.receive_btn_xpath = None
        self.driver = None

    def login(self):
        pass

    def toBuy(self):
        print( '切换到我要买页面' )
        self.driver.get( self.toBuy_url )
        time.sleep(3)

    def queue_task(self):
        pass

    def wait_task(self):
        pass

    def check_status(self):
        pass

    def status(self):
        pass

    def start_refresh_thread(self):
        pass