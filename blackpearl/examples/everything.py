from blackpearl.modules import Module
from blackpearl.modules import Clock
from blackpearl.modules import Timer
from blackpearl.modules import Touch
from blackpearl.projects import Project
from blackpearl.things import Dial
from blackpearl.things import Matrix
from blackpearl.things import Motor
from blackpearl.things import Number
from blackpearl.things import Rainbow
from blackpearl.things import Slider
from blackpearl.things import Touch



class Scroller(Touch):
    listening_for = ['touch',]
    hardware_required = [Touch, Matrix, Rainbow,]
    
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
        
class SpeedChanger(Module):
    listening_for = ['dial',]
    hardware_required = [Dial, Matrix]
    
    def receive(self, message):
        value = message['dial']['value']
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
        
class RainbowSetter(Module):
    listening_for = ['matrix',]
    hardware_required = [Matrix, Rainbow,]
    
    def receive(self, message):
        if 'scroller' in message['matrix']:
            status = message['matrix']['scroller']
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
        
class Listener(Module):
    listening_for = ['timer']
    def receive(self, message):
        print(message['timer']['time'])
        
class DiscoLights(Module):
    listening_for = ['slider',]
    hardware_required = [Slider, Rainbow,]
    
    def receive(self, message):
        value = (message['slider']['value'])/1000.0
        red, green, blue = self.rainbow.hue(value)
        self.rainbow.set_all(red, green, blue)
        self.rainbow.update()

class Mover(Module):
    listening_for = ['slider',]
    hardware_required = [Slider, Motor, Motor,]
    
    def receive(self, message):
        value = message['slider']['value']
        if value == 0:
            v = -63
        elif value == 1000:
            v = 63
        else:
            v = int((value - 500)/8)
        
        self.motor1.set_speed(v)
        self.motor2.set_speed(v * -1)

class ClockDisplay(Module):
    listening_for = ['clock',]
    hardware_required = [Number,]
    def receive(self, message):
        tm = message['clock']['as_string']
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