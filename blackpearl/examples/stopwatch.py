from blackpearl.modules import Module
from blackpearl.modules import Timer
from blackpearl.modules import Touch
from blackpearl.projects import Project
from blackpearl.things import Number
from blackpearl.things import Touch


class Stopwatch(Timer):
    
    tick = 0.01
    hardware_required = [Number, Touch,]
    listening_for = ['timer', 'touch',]
    
    def receive(self, message):
        if 'timer' in message:
            tm = message['timer']['time']
            self.number.set_number(tm, precision='00')
            self.number.update()
        elif 'touch' in message:
            buttons = message['touch']['buttons']
            if buttons['1']:
                if self.status == 'RUNNING':
                    self.stop()
                elif self.status == 'STOPPED':
                    self.start()
            if buttons['2'] and self.status == 'STOPPED':
                self.reset()
                self.number.set_number(0)
                self.number.update()
        
        
class MyProject(Project):
    required_modules = [Stopwatch, ]
    

if __name__ == '__main__':
    MyProject()