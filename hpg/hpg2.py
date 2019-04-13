import sys
sys.path.append('..')

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

from base import BASE

from chrome.connect_chrome import Chrome
from ulity import china_time,send_wechat,send_email
import os,time

class HPG(BASE,Chrome):
    def __init__(self,name = 'hpg',debug = False,mobileEmulation = None):
        self.name = name
        self.driver = None

        self.username = os.environ.get( 'HPG_USER' )  # 用户名
        self.password = os.environ.get( 'HPG_PASS' )  #

        self.login_url = 'http://hpg.sqk2.cn/public/apprentice.php/passport/login.html'
        self.task_url= 'http://hpg.sqk2.cn/public/apprentice.php/task/index.html'
        self.submitted_url = 'http://hpg.sqk2.cn/public/apprentice.php/task/submitted.html'
        self.user_url = 'http://hpg.sqk2.cn/public/apprentice.php/user/index.html'


        self.username_id = 'username'
        self.password_id = 'password'
        self.login_button_id = 'login-btn'
        self.normal_task_button_xpath = '//*[@id="normal-task"]'
        self.activity_task_button_xpath = '//*[@id="activity-task"]'
        self.receive_btn_xpath = '//*[@id="operation"]/a[2]'
        self.traffic_task_xpath = '//*[@id="traffic-task"]'

        self.taskInfo = None

    def login(self):
        print( '登陆hpg：{}'.format(self.login_url) )
        self._get( self.login_url )

        # 输入用户名及密码
        username_element = self.driver.find_element_by_id( self.username_id )
        username_element.clear()
        username_element.send_keys( self.username )

        password_element = self.driver.find_element_by_id( self.password_id )
        password_element.clear()
        password_element.send_keys( self.password )

        login_element = self.driver.find_element_by_id( self.login_button_id )
        login_element.click()
        time.sleep( 2 )
        print( '已登陆HPG，完成初始化操作' )

    def queue_task(self):
        try:
            normal_task = self.driver.find_element_by_id('normal-task')
            if normal_task.text == '我要买':
                normal_task.click()
                time.sleep(1)

            activity_task = self.driver.find_element_by_id('activity-task')
            if activity_task.text == '活动单':
                activity_task.click()
                time.sleep(1)
        except:
            print('没找到我要买按钮')

    def checkTask(self):
        self.driver.refresh()
        time.sleep( 3 )
        try:
            self.receiveButton = self.driver.find_element_by_xpath(self.receive_btn_xpath)
            print(self.receiveButton.text)
            if self.receiveButton.text == '领取':
                print('已接到任务，准备领取')
                self.findedReceiveButton = True
                self.taskReceived = False
            else:
                if self.receiveButton.text == '请先验证宝贝':
                    self.taskReceived = True
                    self.findedReceiveButton = False
                    print('任务已领取')
        except:
            self.receiveButton = None
            print(time.time(),'没找到领取按钮，继续等待接收任务')
            time.sleep(10)

    def receiveTask(self):
        #滑动页面
        self.driver.execute_script( "window.scrollTo(0, document.body.scrollHeight);" )

        print( '点击领取按钮' )
        self.receiveButton.click( )
        self.checkTask()

    def getTaskInfo(self):
        key_word = self.driver.find_element_by_id('target').get_attribute('value')
        #print(key_word)
        main_link = self.driver.find_element_by_class_name('main_link').get_attribute('src')
        #print(main_link)
        price = self.driver.find_element_by_class_name('customer_order').text
        remarks_word = self.driver.find_element_by_class_name('remarks_word').text
        #print(price,remarks_word)
        self.taskInfo = {'keyword':key_word,
                         'main_link':main_link,
                         'price':price,
                         'remarks_word':remarks_word,

                         }


    def check_login(self):
        time.sleep( 3 )
        if self.driver.current_url in [self.user_url,self.task_url,self.submitted_url]:
            return True
        else:
            return False

    def check_queued_task(self):
        print('检查已定阅')
        if self.driver.current_url == self.task_url:
            try:
                normal_task = self.driver.find_element_by_id( 'normal-task' )
                activity_task = self.driver.find_element_by_id( 'activity-task' )
                if normal_task.text == '停止' and activity_task.text == '停止':
                    return True
                else:return False

            except: return False

        else:
            print('open:{}'.format(self.task_url))
            self.driver.get(self.task_url)
            time.sleep(5)
            self.check_queued_task()

    def check_queue_task(self):
        print( '检查我要买' )
        if self.driver.current_url == self.task_url:
            try:
                normal_task = self.driver.find_element_by_id( 'normal-task' )
                activity_task = self.driver.find_element_by_id( 'activity-task' )
                if normal_task.text == '我要买' and activity_task.text == '活动单':
                    print( normal_task.text, activity_task.text )
                    return True
                else:return False

            except: return False

        else:
            print('open:{}'.format(self.task_url))
            self.driver.get(self.task_url)
            time.sleep(5)
            self.check_queue_task()

    def check_received_task(self):
        try:
            self.receiveButton = self.driver.find_element_by_xpath(self.receive_btn_xpath)
            if self.receiveButton.text == '领取':
                print('已接到任务，准备领取')
                #self.driver.execute_script( "arguments[0].scrollIntoView(false);", self.receiveButton )
                self.driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)" )
                self.receiveButton.click()
                return True
            else:return False
        except:
            print('没找到领取按钮，继续等待接收任务')
            return False




