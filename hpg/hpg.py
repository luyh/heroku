from state_machine import State, Event, acts_as_state_machine, after, before, InvalidStateTransition
from base import BASE
import sys
sys.path.append('..')
from chrome import connectChrome
from ulity import china_time,send_wechat,send_email
import os
import time
import state
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

@acts_as_state_machine
class HPG(BASE,state.StateMachine):
    initialHPG = State(initial=True)
    hpgChrome = connectChrome(name='hpg')
    hpgChromeConnected = hpgChrome.sucessConnectedToChrome
    hpgLogined = State()
    hpgSubscribedTask = State()
    hpgWaitingTask = State()
    hpgReceiveingTask = State()
    hpgReceivedTask = State()
    hpgWaitingSubmitTask = State()
    hpgCheckedTask = State()

    hpgChromeEvent = Event( from_states=initialHPG,
                                to_state= hpgChromeConnected)
    hpgLoginEvent = Event( from_states=hpgChromeConnected,
                           to_state= hpgLogined)
    hpgCheckingTaskEvent = Event( from_states= (hpgLoginEvent,),
                           to_state= hpgCheckedTask)

    hpgSubscribeTaskEvent = Event( from_states=hpgCheckedTask,
                           to_state= hpgSubscribedTask)
    hpgInitWaitingTaskEvent = Event( from_states=hpgSubscribedTask,
                           to_state= hpgWaitingTask)
    hpgKeepWaitingTaskEvent = Event( from_states=hpgWaitingTask,
                           to_state= hpgWaitingTask)
    hpgReceiveTaskEvent = Event( from_states=hpgWaitingTask,
                           to_state= hpgReceiveingTask)
    hpgSubmitTaskEvent = Event( from_states=(hpgWaitingTask,hpgReceiveingTask),
                           to_state= hpgWaitingSubmitTask)



    def __init__(self,debug = False):
        self.login_url = 'http://hpg.sqk2.cn/public/apprentice.php/passport/login.html'
        self.toBuy_url= 'http://hpg.sqk2.cn/public/apprentice.php/task/index.html'
        self.receive_btn_xpath = '//*[@id="operation"]/a[2]'
        self.findedReceiveButton = False
        self.username = os.environ.get( 'HPG_USER' )  # 用户名
        self.password = os.environ.get( 'HPG_PASS' )  #
        self.taskReceived = False
        self.taskInfo = None
        self.driver = None
        self.debug = debug

    def start(self):
        self.transition(self.hpgChromeEvent,'hpgChromeEvent')

    @before('hpgChromeEvent')
    def new_chrome(self):
        self.hpgChrome.start()
        if self.hpgChrome.connected:
            self.driver = self.hpgChrome.driver
            self.driver.set_window_size(50, 1000)

    @after('hpgChromeEvent')
    def toLogin(self):
        self.transition(self.hpgLoginEvent,'hpgLoginEvent')

    @before('hpgLoginEvent')
    def login(self):
        print( '登陆hpg：{}'.format(self.login_url) )
        self._get( self.login_url )


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

    @after('hpgLoginEvent')
    def toBuyEvent(self):
        self.transition(self.hpgSubscribeTaskEvent,'hpgSubscribeTaskEvent')

    @before('hpgSubscribeTaskEvent')
    def queue_task(self):
        self.toBuy()
        try:
            normal_task = self.driver.find_element_by_id('normal-task')
            if normal_task.text == '我要买':
                normal_task.click()
                time.sleep(1)
            elif normal_task.text == '停止':
                pass

            activity_task = self.driver.find_element_by_id('activity-task')
            if activity_task.text == '活动单':
                activity_task.click()
            elif activity_task.text == '停止':
                pass

        except:
            print('没找到我要买按钮')

    @after('hpgSubscribeTaskEvent')
    def waitTaskEvent(self):
        self.transition(self.hpgInitWaitingTaskEvent,'hpgInitWaitingTaskEvent')

    @before('hpgInitWaitingTaskEvent')
    @before('hpgKeepWaitingTaskEvent')
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

    @after('hpgInitWaitingTaskEvent')
    @after('hpgKeepWaitingTaskEvent')
    @after( 'hpgReceiveTaskEvent' )
    def checkTaskNextEvent(self):
        if self.findedReceiveButton == True:
            self.transition( self.hpgReceiveTaskEvent, 'hpgReceiveTaskEvent' )
        elif self.taskReceived == True:
            self.getTaskInfo()
            print(self.taskInfo)
            self.transition(self.hpgSubmitTaskEvent,'hpgSubmitTaskEvent')
        else:
            self.transition(self.hpgKeepWaitingTaskEvent,'hpgKeepWaitingTaskEvent')


    @before('hpgReceiveTaskEvent')
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

if __name__ == '__main__':
    hpg = HPG(debug= True)
    hpg.start()
