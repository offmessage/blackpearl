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
        
        def col_value(v):
            m = max((min(v, 2400) - 1600)//100, 0)
            return (2**m) - 1
        
        if self.running:
            lcol = col_value(self.left_light)
            rcol = col_value(self.right_light)
            pixels = [lcol,] * 4 + [rcol,] * 4
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
                self.matrix.reset()
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
            if channel == left:
                self.left_light = lux
            elif channel == right:
                self.right_light = lux
            
            if self.left_light < 1500 or self.right_light < 1500:
                # special case caused by small paper and studland table!
                self.left_speed = BASE_SPEED
                self.right_speed = BASE_SPEED
                self.set_speed()
                return
            
            light_difference = self.left_light - self.right_light
            # right > left means left is over the line, so left should stop
            # left > right means right is over the line, so right should stop
            if light_difference < -100:
                self.left_speed = 0
            elif light_difference > 100:
                self.right_speed = 0
            else:
                self.left_speed = BASE_SPEED
                self.right_speed = BASE_SPEED
            self.set_speed()
            
    
    
class MyProject(Project):
    required_modules = [Robot,]
    

if __name__ == '__main__':
    MyProject()
    
        