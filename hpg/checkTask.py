from state_machine import State, Event, acts_as_state_machine, after, before, InvalidStateTransition
import state
import time


@acts_as_state_machine
class CheckTask(state.StateMachine):
    initialCheckTask = State( initial=True )

    def __init__(self,driver):
        self.driver = driver

def checkTask(self):
    self.driver.refresh()
    time.sleep( 3 )
    try:
        self.receiveButton = self.driver.find_element_by_xpath (self.receive_btn_xpat h)
        print (self.receiveButton.tex t)
        if self.receiveButton.text == '领取':
            print ('已接到任务，准备领取 ')
            self.findedReceiveButton = True
            self.taskReceived = False
        else:
            if self.receiveButton.text == '请先验证宝贝':
                self.taskReceived = True
                self.findedReceiveButton = False
                print ('任务已领取 ')
    except:
        self.receiveButton = None
        print (time.time() ,'没找到领取按钮，继续等待接收任务 ')
        time.sleep (1 0)

