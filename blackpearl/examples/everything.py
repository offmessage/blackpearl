from blackpearl.modules import BaseModule
from blackpearl.modules import Clock
from blackpearl.modules import Timer
from blackpearl.modules import Touch
from blackpearl.projects import Project


class Scroller(Touch):
    listening_for = ['touch',]
    hardware_required = ['touch', 'matrix', 'rainbow',]
    
    def button1_pressed(self):
        self.matrix.reset()
        self.matrix.addText("This is a great example! ")
        self.matrix.scrollspeed = 0.1
        self.matrix.loop = True
        self.matrix.scroll()
        
    def button2_pressed(self):
        self.matrix.scrollspeed = 0.05
        
    def button3_pressed(self):
        self.matrix.reset()
        self.rainbow.reset()
        
    def button4_pressed(self):
        self.matrix.pause()
        
class SpeedChanger(BaseModule):
    listening_for = ['dial',]
    hardware_required = ['dial', 'matrix']
    
    def receive(self, data):
        value = data['dial']['value']
        if value < 200:
            spd = 0.25
        elif value < 400:
            spd = 0.2
        elif value < 600:
            spd = 0.15
        elif value < 800:
            spd = 0.1
        else:
            spd = 0.05
        self.matrix.scrollspeed = spd
        
class RainbowSetter(BaseModule):
    listening_for = ['matrix',]
    hardware_required = ['matrix', 'rainbow',]
    
    def receive(self, data):
        if 'scroller' in data['matrix']:
            status = data['matrix']['scroller']
            if status in ['running', 'step', 'loop']:
                self.rainbow.set_all(0, 255, 0)
                self.rainbow.update()
            elif status in ['paused', 'stopped']:
                self.rainbow.set_all(255, 0, 0)
                self.rainbow.update()
            
class MyTimer(Timer):
    tick = 0.1
    def setup(self):
        self.start()
        
class Listener(BaseModule):
    listening_for = ['timer']
    def receive(self, data):
        print(data['timer']['time'])
        
class DiscoLights(BaseModule):
    listening_for = ['slider',]
    hardware_required = ['slider', 'rainbow',]
    
    def receive(self, data):
        value = (data['slider']['value'])/1000.0
        red, green, blue = self.rainbow.hue(value)
        self.rainbow.set_all(red, green, blue)
        self.rainbow.update()

class Mover(BaseModule):
    listening_for = ['slider',]
    hardware_required = ['slider', 'motor', 'motor',]
    
    def receive(self, data):
        value = data['slider']['value']
        if value == 0:
            v = -63
        elif value == 1000:
            v = 63
        else:
            v = int((value - 500)/8)
        
        self.motor1.set_speed(v)
        self.motor2.set_speed(v * -1)

class ClockDisplay(BaseModule):
    listening_for = ['clock',]
    hardware_required = ['number',]
    def receive(self, data):
        tm = data['clock']['as_string']
        self.number.set_digit(0, tm[0])
        self.number.set_digit(1, tm[1])
        if tm[2] == ":":
            self.number.colon = 1
        else:
            self.number.colon = 0
        self.number.set_digit(2, tm[3])
        self.number.set_digit(3, tm[4])
        self.number.update()
        

class MyProject(Project):
    required_modules = [Scroller, SpeedChanger, RainbowSetter, 
                        MyTimer, Listener, DiscoLights, Mover, Clock, 
                        ClockDisplay, ]
    

if __name__ == '__main__':
    MyProject()