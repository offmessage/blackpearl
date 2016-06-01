from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Light
from blackpearl.things import Matrix
from blackpearl.things import Motor
from blackpearl.things import Rainbow
from blackpearl.things import Touch


class Robot(Module):
    
    listening_for = ['light', 'touch',]
    hardware_required = [Light, Light, Matrix, Motor, Motor, Rainbow, Touch,]
    
    right_light = 0
    left_light = 0
    right_speed = 20
    left_speed = 20
    running = True
    
    def setup(self):
        self.rainbow.reset()
        self.rainbow.set_all(255, 255, 255)
        self.rainbow.update()
        self.matrix.reset()
        #self.matrix.addText("Hello Grace! Happy birthday! Have a lovely day! ")
        #self.matrix.scrollspeed = 0.1
        #self.matrix.loop = True
        #self.matrix.scroll()
        self.set_speed()
        
    def set_speed(self):
        if self.running:
            self.motor1.set_speed(self.left_speed * -1)
            self.motor2.set_speed(self.right_speed)
        else:
            self.motor1.set_speed(0)
            self.motor2.set_speed(0)
        
    def receive(self, message):
        if 'touch' in message:
            self.right_speed = 0
            self.left_speed = 0
            self.running = False
            self.set_speed()
            self.rainbow.set_all(0,0,0)
            self.rainbow.update()
            
        elif 'light' in message:
            left = 4
            right = 5
            channel = message['light']['channel']
            lux = message['light']['lux']
            if channel == 4:
                self.left_light = lux
            elif channel == 5:
                self.right_light = lux
            
            if self.left_light < 1600 or self.right_light < 1500:
                # special case caused by small paper and studland table!
                return
            test = self.left_light - self.right_light
            # right > left means left is over the line, so left should stop
            # left > right means right is over the line, so right should stop
            if abs(test) > 100:
                if test < 0:
                    self.left_speed = 0
                elif test > 0:
                    self.right_speed = 0
            else:
                self.left_speed = 20
                self.right_speed = 20
            self.set_speed()
            
    
    
class MyProject(Project):
    required_modules = [Robot,]
    

if __name__ == '__main__':
    MyProject()
    
        