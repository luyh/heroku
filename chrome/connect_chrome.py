from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from chrome import mywebdriver
from selenium.common.exceptions import WebDriverException
import pickle
import time,sys
from transitions import Machine

# 打印系统系统
systerm = sys.platform
print( '系统类型:', systerm )

class Chrome():
    mobileEmulation = None
    def __init__(self,name = 'chrome',mobileEmulation = None):
        self.name = name
        self.driver = None
        self.mobileEmulation = mobileEmulation

    def connectChrome(self):
        print( '正在读取{}.data 尝试连接chrome:{}'.format( self.name,self.name ) )
        try:
            f = open( "{}.data".format(self.name), 'rb' )
            # 从文件中载入对象
            params = pickle.load( f )
            # print( params )
            browser = mywebdriver.myWebDriver( service_url=params["server_url"],
                                               session_id=params["session_id"] )
            try:
                print(browser.title)
                print( '已连上chrome参数为:{}'.format( params ) )
                self.driver = browser
                return True
            except WebDriverException:
                print( 'chrome not reachable，连接chrome失败' )
                return False

        except FileNotFoundError:
            print('没找到：{}.data文件".format(self.name)')
            return False

    def newChrome(self):
        options = webdriver.ChromeOptions()
        if self.mobileEmulation != None:
            options.add_experimental_option( 'mobileEmulation', self.mobileEmulation )

        # 连接Chrome
        print(u'正在新建chrome浏览器...')
        if systerm.startswith('darwin'):

            driver = webdriver.Chrome(executable_path='/Users/Hebbelu/Downloads/chromedriver', \
                                      chrome_options=options)
        elif systerm.startswith('linux'):
            driver = webdriver.Chrome(chrome_options=options)

        elif systerm.startswith('win32'):
            driver = webdriver.Chrome(executable_path='C:/Users/Administrator/fast-retreat-53401/chrome/chromedriver.exe', chrome_options=options)
        time.sleep(3)

        print(u'已新建chrome浏览器，并成功连接')
        self.driver = driver

        params = {}
        params["session_id"] = driver.session_id
        params["server_url"] = driver.command_executor._url

        print('正在保存chrome参数至{}.data' .format(self.name))
        f = open( "{}.data".format(self.name), 'wb' )
        # 转储对象至文件
        pickle.dump( params, f )
        f.close()
        print('已保存chrome参数至{}.data' .format(self.name))


if __name__ == '__main__':
    states = ['initialChrome','NewedChrome','ConnectedChrome']

    transitions = [
        {'trigger': 'connect',
         'source': 'initialChrome',
         'dest': 'ConnectedChrome',
         'conditions': 'connectChrome'
         },

        {'trigger': 'new',
         'source': 'initialChrome',
         'dest': 'NewedChrome',
         'before':'newChrome'
        },
    ]

    chrome = Chrome()

    machine = Machine( chrome, states=states, transitions=transitions, initial='initialChrome' )

    print(chrome.state)
    chrome.connect()
    print(chrome.state)
    if chrome.state != 'ConnectedChrome':
        chrome.new()
        print( chrome.state )



