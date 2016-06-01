from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Light
from blackpearl.things import Matrix
from blackpearl.things import Motor
from blackpearl.things import Rainbow
from blackpearl.things import Touch

BASE_SPEED = 32

class Robot(Module):
    
    listening_for = ['light', 'touch',]
    hardware_required = [Light, Light, Matrix, Motor, Motor, Rainbow, Touch,]
    
    right_light = 0
    left_light = 0
    right_speed = BASE_SPEED
    left_speed = BASE_SPEED
    running = True
    
    def setup(self):
        self.rainbow.reset()
        self.rainbow.set_all(255, 255, 255)
        self.rainbow.update()
        self.matrix.reset()
        self.set_speed()
        
    def set_speed(self):
        if self.running:
            self.motor1.set_speed(self.left_speed * -1)
            self.motor2.set_speed(self.right_speed)
        else:
            self.motor1.set_speed(0)
            self.motor2.set_speed(0)
        self.calc_graph()
        
    def calc_graph(self):
        
        leftmax = max((min(self.left_light, 2400) - 1600)//100, 0)
        rightmax = max((min(self.right_light, 2400) - 1600)//100, 0)
        pixels = [0,
                  ((2**leftmax) - 1),
                  ((2**leftmax) - 1),
                  0,
                  0,
                  ((2**rightmax) - 1),
                  ((2**rightmax) - 1),
                  0,
                  ]
        if self.running:
            self.matrix.update(pixels)
        
    def receive(self, message):
        if 'touch' in message:
            if message['touch']['buttons']['1']:
                self.right_speed = BASE_SPEED
                self.left_speed = BASE_SPEED
                self.running = True
                self.set_speed()
                self.rainbow.set_all(255,255,255)
                self.rainbow.update()
            elif message['touch']['buttons']['4']:
                self.right_speed = 0
                self.left_speed = 0
                self.running = False
                self.set_speed()
                self.rainbow.set_all(0,0,0)
                self.rainbow.update()
                self.matrix.reset()
            
        elif 'light' in message:
            left = 4
            right = 5
            channel = message['light']['channel']
            lux = message['light']['lux']
            if channel == 4:
                self.left_light = lux
            elif channel == 5:
                self.right_light = lux
            
            if self.left_light < 1500 or self.right_light < 1500:
                # special case caused by small paper and studland table!
                self.left_speed = BASE_SPEED
                self.right_speed = BASE_SPEED
                self.set_speed()
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
                self.left_speed = BASE_SPEED
                self.right_speed = BASE_SPEED
            self.set_speed()
            
    
    
class MyProject(Project):
    required_modules = [Robot,]
    

if __name__ == '__main__':
    MyProject()
    
        