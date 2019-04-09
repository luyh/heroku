from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from state_machine import State, Event, acts_as_state_machine, after, before, InvalidStateTransition
import mywebdriver
from selenium.common.exceptions import WebDriverException
import state
import pickle
import sys
import time

# 打印系统系统
systerm = sys.platform
print( '系统类型:', systerm )

@acts_as_state_machine
class connectChrome(state.StateMachine):
    initialChrome = State(initial=True)
    tryedConnectChrome = State()
    failConnectedToChrome = State()
    sucessConnectedToChrome = State()

    tryConnectChromeEvent = Event( from_states=initialChrome,to_state= tryedConnectChrome)
    newChromeEvent = Event( from_states=tryedConnectChrome, to_state= sucessConnectedToChrome)
    reloadChromeEvent = Event( from_states=tryedConnectChrome, to_state= sucessConnectedToChrome)

    def __init__(self,name = 'chrome'):
        self.name = name
        self.driver = None
        self.connected = False
        self.debug = False
        print('新建连接chrome:{}'.format(name))


    def start(self):
        self.transition(self.tryConnectChromeEvent,'tryConnectChromeEvent')

    @before( 'tryConnectChromeEvent' )
    def tryConnect(self):

        try:
            f = open( "{}.data".format(self.name), 'rb' )
            # 从文件中载入对象
            params = pickle.load( f )
            # print( params )
            browser = mywebdriver.myWebDriver( service_url=params["server_url"],
                                               session_id=params["session_id"] )
            try:
                browser.get( 'http://www.baidu.com' )
                print( '已连上chrome:{}'.format( params ) )
                self.driver = browser
                self.connected = True
            except WebDriverException:
                print( 'Message: chrome not reachable，连接chrome失败' )

        except FileNotFoundError:
            print('没找到：{}.data文件".format(self.name)')




    @after( 'tryConnectChromeEvent' )
    def checkConnect(self):
        if self.connected == True:
            self.transition(self.reloadChromeEvent,'reloadChromeEvent')
        else:
            self.transition(self.newChromeEvent,'newChromeEvent')

    @before('reloadChromeEvent')
    def reloadChrome(self):
        print('连接现有chrome:{}'.format(self.name))

    @after('reloadChromeEvent')
    def finish_reloadChrome(self):
        print('已完成连接现有chrome:{}'.format(self.name))

    @before('newChromeEvent')
    def newChrome(self):
        mobileEmulation = {'deviceName': 'iPhone X'}
        options = webdriver.ChromeOptions()
        options.add_experimental_option( 'mobileEmulation', mobileEmulation )

        # 连接Chrome
        print(u'正在连接chrome浏览器...')
        if systerm.startswith('darwin'):

            driver = webdriver.Chrome(executable_path='/Users/Hebbelu/Downloads/chromedriver', \
                                      chrome_options=options)
        elif systerm.startswith('linux'):
            driver = webdriver.Chrome(chrome_options=options)

        elif systerm.startswith('win32'):
            driver = webdriver.Chrome(executable_path='.\chromedriver.exe', chrome_options=options)
        driver.set_window_size( 50, 800 )
        time.sleep(3)

        print(u'已打开chrome浏览器，并成功连接')
        self.driver = driver

        params = {}
        params["session_id"] = driver.session_id
        params["server_url"] = driver.command_executor._url

        f = open( "{}.data".format(self.name), 'wb' )
        # 转储对象至文件
        pickle.dump( params, f )
        f.close()

        self.connected = True

    @after('newChromeEvent')
    def finish_newChrome(self):
        print('已新建chrome:{},等待连接外部事件'.format(self.name))

    def getChrome(self):
        return self.driver

if __name__ == '__main__':
    connect_chrome = connectChrome(name='hpg')
    #connect_chrome.debug = True
    connect_chrome.start()
    if connect_chrome.connected == True:
        driver = connect_chrome.getChrome()
        url = 'http://www.baidu.com'
        print('打开百度:{}'.format(url))
        driver.get(url)
        print( '已打开百度:{}'.format(url) )

    else:
        print('未连上chrome')