from base import BASE
from chrome.connect_chrome import Chrome
from ulity import china_time,send_email
import os,time
from transitions import Machine

class ZKB(BASE,Chrome):
    states = ['initial',
              'connectedChrome',
              'loginZKB',
              'quereedTask',
              'receivedTask',

              ]

    def __init__(self, name='zkb', debug=False, mobileEmulation=None):
        self.name = name
        self.driver = None

        self.username = os.environ.get( 'HPG_USER' )  # 用户名
        self.password = os.environ.get( 'HPG_PASS' )  #

        self.login_url = 'http://zhuankeban.com/jsp/Mobile/apprentice/ApprenticeLogin.jsp'
        self.task_url = 'http://zhuankeban.com/webmobile/apprentice/toBuy.do'
        self.submitted_url = 'http://zhuankeban.com//jsp/Mobile/apprentice/Task.jsp?ut=apprentice'
        self.user_url = 'http://zhuankeban.com/jsp/Mobile/apprentice/ApprenticeInfo.jsp'
        self.receive_url = ''

        self.username_id = 'user_account'
        self.password_id = 'user_password'
        self.login_button_id = 'Signin'
        self.receive_btn_xpath = '/html/body/section/div[3]/div/div[2]'

        self.taskInfo = None
        self.taskInfoFlag = False

        self.now = china_time.ChinaTime()

        self.machine = Machine( model=self, states=ZKB.states, initial='initial' )
        self.machine.add_transition( 'connect_chrome', 'initial', 'connectedChrome', conditions='connectChrome' )
        self.machine.add_transition( 'CheckLogin', '*', 'loginZKB',
                                conditions='check_login' )

        self.machine.add_transition( 'QuereTask', '*', 'quereedTask',
                                conditions='queue_task' )

        self.machine.add_transition( 'ReceiveTask', '*', 'receivedTask',
                                conditions='receive_task' )

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
            if '666' in self.driver.page_source:
                if self.login():
                    return True
            else:
                return True
        else:
            if self.login():
                return True

    def queue_task(self):
        # print( '检查我要买' )
        if self.driver.current_url == self.task_url:
            try:
                task_element = self.driver.find_element_by_id( 'queue-up-task' )

                if task_element.text == '停止':
                    return True

                elif task_element.text == '我要买' :
                    task_element.click()
                    time.sleep( 1 )
                    print( self.now.getChinaTime(), '已订阅任务' )
                    return True

                else:
                    return False

            except:
                print( '没找到我要买按钮' )
                return False

        else:
            print( 'open:{}'.format( self.task_url ) )
            self.driver.get( self.task_url )
            time.sleep( 3 )
            self.queue_task()

    def receive_task(self):
        # print('检查领取状态')
        if self.driver.current_url == self.task_url:
            try:
                self.receiveButton = self.driver.find_element_by_xpath( self.receive_btn_xpath )

                if self.receiveButton.text == '请先验证宝贝':
                    return True

                elif self.receiveButton.text == '领取':
                    print( '已接到任务，准备领取' )
                    # self.driver.execute_script( "arguments[0].scrollIntoView(false);", self.receiveButton )
                    self.driver.execute_script( "window.scrollTo(0,document.body.scrollHeight)" )
                    self.receiveButton.click()

                    print( '已领取任务，快做单' )
                    self.getTaskInfo()
                    print( self.taskInfo )
                    send_email.send_email( '接到hpg任务', self.taskInfo )

                    time.sleep( 3 )

                    self.receive_task()

            except:
                # print('没找到领取按钮，继续等待接收任务')
                return False

        else:
            print( 'open:{}'.format( self.task_url ) )
            self.driver.get( self.task_url )
            time.sleep( 5 )
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

if __name__ == '__main__':
    zkb = ZKB()

    print( zkb.state )
    old_state = zkb.state

    zkb.connect_chrome()

    while (1):
        zkb.CheckLogin()
        zkb.QuereTask()
        zkb.ReceiveTask()

        if zkb.state != old_state:
            print( zkb.now.getChinaTime(), zkb.state )

        old_state = zkb.state
        zkb.driver.refresh()
        time.sleep( 15 )
