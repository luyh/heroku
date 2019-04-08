from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from hpg.base import BASE
import os
import time
from chrome2 import chrome


class HPG(BASE):
    def __init__(self):
        self.login_url = 'http://hpg.sqk2.cn/public/apprentice.php/passport/login.html'
        self.toBuy_url= 'http://hpg.sqk2.cn/public/apprentice.php/task/index.html'
        self.receive_btn_xpath = '//*[@id="operation"]/a[2]'
        self.username = os.environ.get( 'HPG_USER' )  # 用户名
        self.password = os.environ.get( 'HPG_PASS' )  #
        self.driver = None

    def new_chrome(self):
        self.driver = chrome.chrome()

    def connect_chrome(self,port):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{}".format(port))
        # driver就是当前浏览器窗口
        driver = webdriver.Chrome(chrome_options=chrome_options)

    def login(self):
        print( '打开hpg' )
        self.driver.get( self.login_url )
        print( self.driver.title )

        # 输入用户名及密码
        print( '输入用户名及密码...' )
        username_element = self.driver.find_element_by_id( 'username' )
        username_element.clear()
        username_element.send_keys( self.username )


        password_element = self.driver.find_element_by_id( 'password' )
        password_element.clear()
        password_element.send_keys( self.password )

        print( '点击登陆...' )
        login_element = self.driver.find_element_by_id( 'login-btn' )
        login_element.click()
        time.sleep( 2 )
        print( '已登陆HPG，完成初始化操作' )


    def queue_task(self):
        try:
            normal_task = self.driver.find_element_by_id('normal-task')
            normal_task.click()
            time.sleep(1)
            activity_task = self.driver.find_element_by_id('activity-task')
            activity_task.click()

        except:
            print('没找到我要买按钮')


    def wait_task(self):
        self.driver.refresh()
        time.sleep( 3 )

        try:
            #recieveBut 定位错
            receiveBut = self.driver.find_element_by_xpath(self.receive_btn_xpath)
            print('点击领取按钮')
            print(receiveBut.text)
            ActionChains(self.driver).click(receiveBut).perform()
            self.status = 'receive_task'
        except:
            print('没找到领取按钮')

        def check_status(self):
            pass

        def run(self):
            pass

if __name__ == '__main__':
    hpg = HPG()