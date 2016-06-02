from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Number
from blackpearl.things import Stopwatch
from blackpearl.things import Touch


class MyStopwatch(Module):
    
    hardware_required = [Number, Touch,]
    software_required = [Stopwatch,]
    listening_for = ['stopwatch', 'touch',]
    
    def setup(self):
        self.number.set_number(0.0, precision='00')
        self.number.update()
        
    def receive(self, message):
        if 'stopwatch' in message:
            tm = message['stopwatch']['time']
            self.number.set_number(tm, precision='00')
            self.number.update()
        
        elif 'touch' in message:
            buttons = message['touch']['buttons']
            if buttons['1'] and self.stopwatch.status == 'STOPPED':
                self.stopwatch.start()
            elif buttons['1'] and self.stopwatch.status == 'RUNNING':
                self.stopwatch.stop()
                self.stopwatch.reset()
            elif buttons['2'] and self.stopwatch.status in ['PAUSED', 'RUNNING']:
                self.stopwatch.pause()
            elif buttons['4'] and self.stopwatch.status in ['PAUSED', 'STOPPED']:
                self.stopwatch.reset()
                self.number.set_number(0.0, precision='00')
                self.number.update()
        
        
class MyProject(Project):
    modules_required = [MyStopwatch, ]
    

if __name__ == '__main__':
    MyProject()