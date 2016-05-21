from blackpearl.projects import Project

from blackpearl.modules import Module
from blackpearl.modules import Timer
from blackpearl.modules import Touch


class Stopwatch(Timer):
    
    tick = 0.01
    hardware_required = ['number', 'touch']
    listening_for = ['timer', 'touch']
    
    def receive(self, data):
        if 'timer' in data:
            tm = data['timer']['time']
            self.number.set_number(tm)
            self.number.update()
        elif 'touch' in data:
            buttons = data['touch']['buttons']
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