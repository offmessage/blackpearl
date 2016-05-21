from blackpearl.modules import BaseModule
from blackpearl.modules import Timer
from blackpearl.projects import flotilla


class MyTimer(Timer):
    tick = 0.1
    def setup(self):
        self.start()
        
class Listener(BaseModule):
    listening_for = ['timer']
    def receive(self, data):
        print(data['timer']['time'])
        

if __name__ == '__main__':
    flotilla.add_module(MyTimer)
    flotilla.add_module(Listener)
    flotilla.run()
    