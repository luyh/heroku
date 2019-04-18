from .base import BASE
from .chrome.connect_chrome import Chrome
from .ulity import china_time,send_email
import os,time



class ZKB(BASE):
    def __init__(self, name='zkb', debug=False, mobileEmulation=None):
        self.name = name
        self.driver = None

        self.username = os.environ.get( 'HPG_USER' )  # 用户名
        self.password = os.environ.get( 'HPG_PASS' )  #

        self.login_url = 'http://zhuankeban.com/jsp/Mobile/apprentice/ApprenticeLogin.jsp'
        self.task_url = 'http://zhuankeban.com/webmobile/apprentice/toBuy.do'
        self.submitted_url = 'http://zhuankeban.com//jsp/Mobile/apprentice/Task.jsp?ut=apprentice'
        self.user_url = 'http://zhuankeban.com/jsp/Mobile/apprentice/ApprenticeInfo.jsp'

        self.username_id = 'user_account'
        self.password_id = 'user_password'
        self.login_button_id = 'Signin'
        self.receive_btn_xpath = '/html/body/section/div[3]/div/div[2]'

        self.taskInfo = None
        self.taskInfoFlag = False

        self.now = china_time.ChinaTime()

    def login(self):
        if self.driver.current_url in self.login_url:
            self.driver.refresh()
            time.sleep( 5 )
            try:
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

                return True

            except:
                print( self.now.getChinaTime(), '登陆失败' )
                return False

        else:
            print( '登陆zkb：{}'.format( self.login_url ) )
            self.driver.get(self.login_url)
            time.sleep( 3 )
            self.login()

    def check_login(self):
        if self.driver.current_url in [self.user_url,self.task_url,self.submitted_url]:
            return True
        else:
            if self.login():
                return True

    def queue_task(self):
        try:
            receive_btn = self.driver.find_element_by_id('queue-up-task')
            receive_btn.click()
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