from state_machine import State, Event, acts_as_state_machine, after, before, InvalidStateTransition

class StateMachine():
    def __init__(self):
        self.debug = False
    def transition(self, event,name='event'):
        try:
            if self.debug :self.print_before_state()
            #print('transition from {} to {}'.format(event.from_states, event.to_state))
            if self.debug:print('执行事件：{}'.format(name))
            event()
            if self.debug:self.print_after_state(name)
        except InvalidStateTransition as err:
            #print('Error: transition from {} to {} failed'.format(event.from_states, event.to_state))
            pass

    def print_before_state(self):
        print('当前状态为：{}'.format(self.current_state))

    def print_after_state(self,name):
        print('已完成事件：{}\状态为：{}'.format(name,self.current_state))