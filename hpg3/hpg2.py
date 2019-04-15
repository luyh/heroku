# import sys
# sys.path.append('..')

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

from base import BASE

from chrome.connect_chrome import Chrome
from ulity import china_time,send_wechat,send_email
import os,time

import threading

threadLock = threading.Lock()
threads = []


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
        self.taskInfoFlag = False

    def login(self):
        if self.driver.current_url in [self.user_url,self.task_url,self.submitted_url]:
            return True
        else:
            if self.driver.current_url in self.login_url:
                try:
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

                    return True
                except:
                    return False

            else:
                print( '登陆hpg：{}'.format( self.login_url ) )
                self.driver.get(self.login_url)
                time.sleep( 3 )
                self.login()

    def check_logout(self):
        if self.driver.current_url in [self.user_url,self.task_url,self.submitted_url]:
            return False
        else:
            self.login()
            return True

    def queue_task(self):
        #print( '检查我要买' )
        if self.driver.current_url == self.task_url:
            try:
                normal_task = self.driver.find_element_by_id( 'normal-task' )
                activity_task = self.driver.find_element_by_id( 'activity-task' )

                if normal_task.text == '停止' and activity_task.text == '停止':
                    return True

                elif normal_task.text == '我要买' and activity_task.text == '活动单':
                    normal_task.click()
                    time.sleep( 1 )
                    activity_task.click()
                    time.sleep( 1 )
                    return True

                else:return False

            except: return False

        else:
            print('open:{}'.format(self.task_url))
            self.driver.get(self.task_url)
            time.sleep(3)
            self.queue_task()

    def receive_task(self):
        #print('检查领取状态')
        if self.driver.current_url == self.task_url:
            try:
                self.receiveButton = self.driver.find_element_by_xpath(self.receive_btn_xpath)

                if self.receiveButton.text == '请先验证宝贝':
                    print( '已领取任务，快做单' )
                    if self.taskInfoFlag:
                        self.getTaskInfo()
                        print( self.taskInfo )
                        send_wechat.send_wechat( '接到hpg任务', self.taskInfo )
                        self.taskInfoFlag = False

                    return True

                elif self.receiveButton.text == '领取':
                    print('已接到任务，准备领取')
                    #self.driver.execute_script( "arguments[0].scrollIntoView(false);", self.receiveButton )
                    self.driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)" )
                    self.receiveButton.click()

                    time.sleep(3)

                    self.taskInfoFlag = True
                    self.receive_task()

            except:
                #print('没找到领取按钮，继续等待接收任务')
                return False

        else:
            print('open:{}'.format(self.task_url))
            self.driver.get(self.task_url)
            time.sleep(5)
            self.receive_task()



    def getTaskInfo(self):
        key_word = self.driver.find_element_by_xpath( '//*[@id="task-container"]/div[2]/div/input').get_attribute( 'value' )
        #print(key_word)
        main_link = self.driver.find_element_by_xpath( '//*[@id="task-container"]/div[3]/img').get_attribute( 'src' )
        #print(main_link)
        price = self.driver.find_element_by_xpath( '//*[@id="task-container"]/div[4]' ).text
        remarks_word = self.driver.find_element_by_xpath( '//*[@id="goods-validate-hint"]' ).text
        #print(price,remarks_word)
        self.taskInfo = {'keyword': key_word,
                         'main_link': main_link,
                         'price': price,
                         'remarks_word': remarks_word,

                         }





