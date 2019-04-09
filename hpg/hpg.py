from state_machine import State, Event, acts_as_state_machine, after, before, InvalidStateTransition
from base import BASE
from chrome import connectChrome
import os
import time
import state

@acts_as_state_machine
class HPG(BASE,state.StateMachine):
    initialHPG = State(initial=True)
    hpgChrome = connectChrome('hpg')
    hpgChromeConnected = hpgChrome.sucessConnectedToChrome
    hpgLogined = State()

    hpgChromeEvent = Event( from_states=initialHPG,
                                to_state= hpgChromeConnected)
    hpgLoginEvent = Event( from_states=hpgChromeConnected,
                           to_state= hpgLogined)


    def __init__(self,debug = False):
        self.login_url = 'http://hpg.sqk2.cn/public/apprentice.php/passport/login.html'
        self.toBuy_url= 'http://hpg.sqk2.cn/public/apprentice.php/task/index.html'
        self.receive_btn_xpath = '//*[@id="operation"]/a[2]'
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

    @after('hpgChromeEvent')
    def toLogin(self):
        self.transition(self.hpgLoginEvent,'hpgLoginEvent')

    @before('hpgLoginEvent')
    def login(self):
        print( '登陆hpg：{}'.format(self.login) )
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

    @after('hpgLoginEvent')
    def toBuy(self):
        #TODO:准备去接任务
        print('准备去接任务')


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
            receiveBut.click()
        except:
            print('没找到领取按钮')

        def check_status(self):
            pass

        def run(self):
            pass

if __name__ == '__main__':
    hpg = HPG(debug= True)
    hpg.start()
