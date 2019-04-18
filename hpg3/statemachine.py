from hpg2 import HPG
from transitions.extensions import HierarchicalMachine as Machine
from states import states
import time
import threading
from ulity import china_time


# # Set up logging; The basic log level will be DEBUG
# import logging
# logging.basicConfig(level=logging.DEBUG)
# # Set transitions' log level to INFO; DEBUG messages will be omitted
# logging.getLogger('transitions').setLevel(logging.INFO)

threadLock = threading.Lock()
threads = []

hpg = HPG()
machine = Machine( hpg, states=states,initial='initial' )
####
machine.add_transition('connect_chrome','initial','connectedChrome',conditions='connectChrome')

#####
machine.add_transition('CheckLogin','*','loginHPG',
                       conditions= 'check_login')

machine.add_transition('QuereTask',['loginHPG','quereedTask','receivedTask'],'quereedTask',
                       conditions='queue_task')

machine.add_transition('ReceiveTask',['loginHPG','quereedTask','receivedTask'],'receivedTask',
                       conditions= 'receive_task')

print(hpg.state)
old_state = hpg.state

hpg.connect_chrome()
time.sleep(2)
hpg.driver.refresh()
time.sleep(3)

now = china_time.ChinaTime()

while(1):
    if hpg.state != old_state:
        print(now.getChinaTime(), hpg.state )

    hpg.CheckLogin()
    if hpg.is_loginHPG():
        hpg.QuereTask()
        hpg.ReceiveTask()


    old_state = hpg.state
    time.sleep(30)
    hpg.driver.refresh()

class ReceivingTaskThread(threading.Thread):
    def __init__(self,hpg,delay = 10):
        threading.Thread.__init__(self)
        self.threadID = 'ReceivingTaskThread'
        self.delay = delay
        self.hpg = hpg

        self.hpg.connect_chrome()
        print(hpg.state)

        self.hpg.driver.refresh()
        time.sleep(5)

        self.hpg.Login()
        print( hpg.state )

        self.hpg.QuereTask()
        print( hpg.state )

        self.hpg.start_refresh_thread( 30 )

    def run(self):
        now = china_time.ChinaTime()
        old_state = hpg.state

        while(1):
            if hpg.state != old_state:
                print(now.getChinaTime(), hpg.state )

            threadLock.acquire()
            self.hpg.CheckLogOut()
            self.hpg.QuereTask()
            self.hpg.ReceiveTask()

            threadLock.release()

            old_state = hpg.state
            time.sleep(self.delay)

# receivingTaskThread = ReceivingTaskThread(hpg)
# receivingTaskThread.start()

print('End')