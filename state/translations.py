from transitions import Machine
import time
from hpg import HPG

hpg = HPG()


#The states argument defines the name of states
states=['start', 'login', 'toBuy','queueTask', 'waitTask','receiveTask','submitTask','failLogin']

# The trigger argument defines the name of the new triggering method
transitions = [
    {'trigger': 'login', 'source': 'start', 'dest': 'login' },
    {'trigger': 'toBuy', 'source': 'login', 'dest': 'toBuy'},
    {'trigger': 'quereTask', 'source': 'toBuy', 'dest': 'waitTask'},
    {'trigger': 'receiveTask', 'source': 'waitTask', 'dest': 'receiveTask'},
    {'trigger': 'sendWechat', 'source': 'receiveTask', 'dest': 'submiteTask'},


]

machine = Machine(model=hpg, states=states, transitions=transitions, initial='start')

hpg.driver.set_window_size(10,800)
hpg.login()
# Test
def trigger():
    pass


