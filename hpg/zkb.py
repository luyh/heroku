from selenium.webdriver.common.action_chains import ActionChains
from hpg.base import BASE
import os
import time
from chrome2 import chrome


class ZKB(BASE):
    def __init__(self):
        self.login_url ="http://zhuankeban.com/jsp/Mobile/apprentice/ApprenticeLogin.jsp"
        self.toBuy_url = 'http://zhuankeban.com/webmobile/apprentice/toBuy.do'
        self.receive_btn_xpath = '/html/body/section/div[3]/div/div[2]'
        self.driver = chrome.chrome()
        self.status = None

    def login(self):
        # 打开网页
        print( '登陆HPG...' )
        self.driver.get( self.login_url )
        print( self.driver.title )

        print( '输入用户名及密码...' )
        username = os.environ.get( 'HPG_USER' )  # 用户名
        username_element = self.driver.find_element_by_id( 'user_account' )
        username_element.clear()
        username_element.send_keys( username )

        password = os.environ.get( 'HPG_PASS' )  #
        password_element = self.driver.find_element_by_id( 'user_password' )
        password_element.clear()
        password_element.send_keys( password )

        print( '点击登陆...' )
        sighinButton = self.driver.find_element_by_id( 'Signin' )
        sighinButton.click()
        time.sleep( 2 )
        print( '已登陆zkb' )

        self.status = 'tuBuy'

    def queue_task(self):
        try:
            receive_btn = self.driver.find_element_by_id('queue-up-task')
            receive_btn.click()
            self.status = 'wait_task'
        except:
            print('没找到我要买按钮')

    def wait_task(self):
        self.driver.refresh()
        time.sleep(3)
        try:
            receiveBut = self.driver.find_element_by_xpath(self.receive_btn_xpath )
            print( receiveBut.text )
            if receiveBut.text == "领取":
                print( '点击领取' )
                ActionChains( self.driver ).click( receiveBut ).perform()
                self.status = 'receive_task'
        except:
            print( '没找到领取按钮' )
            self.status = 'check_status'

    def check_status(self):
        self.driver.refresh()
        time.sleep( 3 )
        if '{"code":"666","msg":"登录失效","success":false}' in self.driver.page_source:
            self.status =  'error'
        else:
            self.status =  'wait_task'

    def run(self):
        pass