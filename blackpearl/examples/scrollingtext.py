from blackpearl.modules import Module
from blackpearl.modules import Touch
from blackpearl.projects import Project
from blackpearl.things import Dial
from blackpearl.things import Matrix
from blackpearl.things import Rainbow
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
    hardware_required = [Dial, Matrix,]
    
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
        
        
class Listener(Module):
    listening_for = ['matrix',]
    hardware_required = [Matrix, Rainbow,]
    
    def receive(self, message):
        if 'scroller' in data['matrix']:
            status = message['matrix']['scroller']
            if status in ['running', 'step', 'loop']:
                self.rainbow.set_all(0, 255, 0)
                self.rainbow.update()
            elif status in ['paused', 'stopped']:
                self.rainbow.set_all(255, 0, 0)
                self.rainbow.update()
            

class MyProject(Project):
    modules_required = [Scroller, SpeedChanger, Listener, ]
    

if __name__ == '__main__':
    MyProject()