from hpg2 import HPG
from transitions.extensions import HierarchicalMachine as Machine
from states import states

hpg = HPG()
machine = Machine( hpg, states=states,initial='initial' )
machine.add_transition('connect_chrome','initial','chrome_connected',conditions=['connectChrome'])
machine.add_transition('new_chrome','initial','chrome_newed',before='newChrome')

print( hpg.state )
hpg.connect_chrome()
print(hpg.state)

if hpg.is_initial():
    hpg.new_chrome()
    print( hpg.state )

machine.add_transition('login_hpg', 'chrome', 'loginHPG')
machine.on_enter_loginHPG('login')
hpg.login_hpg()
print( hpg.state )
