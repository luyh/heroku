from chrome2 import chrome
import time

class BASE(object):
    def __init__(self):
        self.login_url = None
        self.toBuy_url = None
        self.status = None
        self.receive_btn_xpath = None
        self.driver = chrome.chrome()

    def login(self):
        pass

    def toBuy(self):
        print( '切换到我要买页面' )
        self.driver.get( self.toBuy_url )
        time.sleep(3)
        self.status = 'quere_task'

    def queue_task(self):
        pass

    def wait_task(self):
        pass

    def check_status(self):
        pass

    def status(self):
        pass

    def start_refresh_thread(self):
        chrome.start_refresh_thread( self.driver, delay=30 )