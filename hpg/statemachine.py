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
machine.add_transition('connect_chrome','initial','chrome_connected',conditions='connectChrome')
machine.add_transition('connect_chrome','initial','chrome_connected',unless='connectChrome',after ='newChrome')

print( hpg.state )
hpg.connect_chrome()
print(hpg.state)

hpg.start_refresh_thread(30)

#####
machine.add_transition('Login', 'chrome', 'loginHPG',conditions='check_login')
machine.add_transition('Login', 'chrome', 'loginHPG',unless='check_login', after='login')

threadLock.acquire()
hpg.Login()
print( hpg.state )

threadLock.release()

####
machine.add_transition('Quere_normal_task','loginHPG','quereedTask',
                       conditions='check_queue_task')
machine.add_transition('Quere_normal_task','loginHPG','quereedTask',
                       conditions='check_queued_task')
machine.add_transition('Quere_normal_task','loginHPG','receivedTask',
                       conditions= 'check_received_task')
machine.add_transition('Quere_normal_task','loginHPG','waitSubmittTask',
                       conditions= 'checkSubmittTask')

###
machine.add_transition('ReceiveTask','quereedTask','receivedTask',
                       conditions= 'check_received_task')
machine.add_transition('ReceiveTask','quereedTask','quereedTask',
                       unless= 'check_received_task')

threadLock.acquire()
hpg.Quere_normal_task()
threadLock.release()
print( hpg.state )

class ReceivingTaskThread(threading.Thread):
    def __init__(self,hpg,delay = 20):
        threading.Thread.__init__(self)
        self.threadID = 'ReceivingTaskThread'
        self.delay = delay
        self.hpg = hpg

    def run(self):
        now = china_time.ChinaTime()

        while(hpg.is_loginHPG or hpg.is_quereedTask):
            print(now.getChinaTime(),'检查接收任务')

            threadLock.acquire()
            self.hpg.ReceiveTask()
            print( hpg.state )
            threadLock.release()

            time.sleep(self.delay)

receivingTaskThread = ReceivingTaskThread(hpg)
receivingTaskThread.start()


print('End')