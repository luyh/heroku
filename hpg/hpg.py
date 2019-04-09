from state_machine import State, Event, acts_as_state_machine, after, before, InvalidStateTransition
from base import BASE
from chrome import connectChrome
import os
import time
import state

@acts_as_state_machine
class HPG(BASE,state.StateMachine):
    initialHPG = State(initial=True)
    hpgChrome = connectChrome(name='hpg')
    hpgChromeConnected = hpgChrome.sucessConnectedToChrome
    hpgLogined = State()
    hpgSubscribedTask = State()
    hpgWaitingTask = State()
    hpgReceiveingTask = State()

    hpgChromeEvent = Event( from_states=initialHPG,
                                to_state= hpgChromeConnected)
    hpgLoginEvent = Event( from_states=hpgChromeConnected,
                           to_state= hpgLogined)
    hpgSubscribeTaskEvent = Event( from_states=hpgLogined,
                           to_state= hpgSubscribedTask)
    hpgInitWaitingTaskEvent = Event( from_states=hpgSubscribedTask,
                           to_state= hpgWaitingTask)
    hpgKeepWaitingTaskEvent = Event( from_states=hpgWaitingTask,
                           to_state= hpgWaitingTask)
    hpgReceiveTaskEvent = Event( from_states=hpgWaitingTask,
                           to_state= hpgReceiveingTask)


    def __init__(self,debug = False):
        self.login_url = 'http://hpg.sqk2.cn/public/apprentice.php/passport/login.html'
        self.toBuy_url= 'http://hpg.sqk2.cn/public/apprentice.php/task/index.html'
        self.receive_btn_xpath = '//*[@id="operation"]/a[2]'
        self.receiveButton = None
        self.username = os.environ.get( 'HPG_USER' )  # 用户名
        self.password = os.environ.get( 'HPG_PASS' )  #

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
            normal_task.click()
            time.sleep(1)
            activity_task = self.driver.find_element_by_id('activity-task')
            activity_task.click()

        except:
            print('没找到我要买按钮')

    @after('hpgSubscribeTaskEvent')
    def waitTaskEvent(self):
        self.transition(self.hpgInitWaitingTaskEvent,'hpgInitWaitingTaskEvent')

    @before('hpgInitWaitingTaskEvent')
    @before('hpgKeepWaitingTaskEvent')
    def wait_task(self):
        self.driver.refresh()
        time.sleep( 3 )
        try:
            self.receiveButton = self.driver.find_element_by_xpath(self.receive_btn_xpath)
        except:
            self.receiveButton = None
            print('没找到领取按钮')

    @after('hpgInitWaitingTaskEvent')
    @after('hpgKeepWaitingTaskEvent')
    def checkTask(self):
        if self.receiveButton == None:
            self.transition(self.hpgKeepWaitingTaskEvent,'hpgKeepWaitingTaskEvent')
        else:
            self.transition(self.hpgReceiveTaskEvent, 'hpgReceiveTaskEvent')

    @before('hpgReceiveTaskEvent')
    def receiveTask(self):
        print('点击领取按钮')
        self.receiveButton.click()
        time.sleep(3)

    @after('hpgReceiveTaskEvent')
    def anotherEvent(self):
        pass

if __name__ == '__main__':
    hpg = HPG(debug= True)
    hpg.start()
