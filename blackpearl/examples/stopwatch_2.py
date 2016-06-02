from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Number
from blackpearl.things import Stopwatch
from blackpearl.things import Touch


class MyStopwatch(Module):
    
    hardware_required = [Number, Touch,]
    software_required = [Stopwatch,]
    listening_for = ['stopwatch', 'touch',]
    
    status = 'STOPPED'
    on = True
    display_time = 0.0
    
    def setup(self):
        self.number.set_number(0.0, precision='00')
        self.number.update()
        
    def receive(self, message):
        if 'stopwatch' in message:
            tm = message['stopwatch']['time']
            if self.status == 'RUNNING':
                self.display_time = tm
                self.number.set_number(tm, precision='00')
                self.number.update()
            elif self.status == 'PAUSED':
                hundredths = int(tm*100)
                if hundredths % 50 == 0:
                    self.on = not self.on
                    if self.on:
                        self.number.set_number(self.display_time, precision='00')
                        self.number.update()
                    else:
                        self.number.reset()
                    
        elif 'touch' in message:
            buttons = message['touch']['buttons']
            if buttons['1'] and self.status == 'STOPPED':
                self.status = 'RUNNING'
                self.stopwatch.start()
            elif buttons['1'] and self.status == 'RUNNING':
                self.status = 'STOPPED'
                self.stopwatch.stop()
                self.stopwatch.reset()
            elif buttons['2'] and self.status == 'RUNNING':
                self.status = 'PAUSED'
            elif buttons['2'] and self.status == 'PAUSED':
                self.status = 'RUNNING'
            elif buttons['4'] and self.status in ['PAUSED', 'STOPPED']:
                self.status = 'STOPPED'
                self.stopwatch.reset()
                self.number.set_number(0.0, precision='00')
                self.number.update()
        
        
class MyProject(Project):
    required_modules = [MyStopwatch, ]
    

if __name__ == '__main__':
    MyProject()