from blackpearl.modules import BaseModule
from blackpearl.modules import Touch
from blackpearl.projects import BaseProject


class Scroller(Touch):
    listening_for = ['touch',]
    hardware_required = ['touch', 'matrix', 'rainbow',]
    
    def button1_pressed(self):
        self.matrix.reset()
        self.matrix.addText("This is a great example!")
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
    
    def data(self, data):
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
        
class Listener(BaseModule):
    listening_for = ['matrix',]
    hardware_required = ['matrix', 'rainbow',]
    
    def data(self, data):
        if 'scroller' in data['matrix']:
            status = data['matrix']['scroller']
            if status in ['running', 'step', 'loop']:
                self.rainbow.set_all(0, 255, 0)
                self.rainbow.update()
            elif status in ['paused', 'stopped']:
                self.rainbow.set_all(255, 0, 0)
                self.rainbow.update()
            

class Project(BaseProject):
    required_modules = [Scroller, SpeedChanger, Listener, ]
    

if __name__ == '__main__':
    Project()