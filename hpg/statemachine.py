from hpg2 import HPG
from transitions.extensions import HierarchicalMachine as Machine
from states import states
import time
from hpg import threadLock,threads
import threading
from ulity import china_time

hpg = HPG()
machine = Machine( hpg, states=states,initial='initial' )
####
machine.add_transition('connect_chrome','initial','connectedChrome',conditions='connectChrome')

#####
machine.add_transition('Login', 'connectedChrome', 'loginHPG',after='login')

machine.add_transition('QuereTask',['loginHPG','quereedTask','receivedTask'],'quereedTask',
                       conditions='queue_task')

machine.add_transition('ReceiveTask',['loginHPG','quereedTask','receivedTask'],'receivedTask',
                       conditions= 'receive_task')

machine.add_transition('CheckLogOut','*','logoutHPG',
                       conditions= 'check_logout')


class ReceivingTaskThread(threading.Thread):
    def __init__(self,hpg,delay = 20):
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

        while(1):
            print(now.getChinaTime(), hpg.state )

            threadLock.acquire()

            self.hpg.QuereTask()
            self.hpg.ReceiveTask()
            self.hpg.CheckLogOut()

            threadLock.release()


            time.sleep(self.delay)

receivingTaskThread = ReceivingTaskThread(hpg)
receivingTaskThread.start()

print('End')