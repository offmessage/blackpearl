from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Rainbow
from blackpearl.things import Touch


class SimpleCombinationLock(Module):
    listening_for = ['touch',]
    hardware_required = [Rainbow, Touch,]
    
    PIN = [1, 4, 3, 1,]
    
    def setup(self):
        self.numbers_pressed = []
        self.attempts = 0
        self.rainbow.reset()
        
    def receive(self, message):
        b = message['touch']['buttons']
        
        if b['1'] and b['4'] and not b['2'] and not b['3']:
            # reset everything
            self.numbers_pressed = []
            self.attempts = 0
            self.rainbow.reset()
            return
        
        # Just single button presses
        if b['1'] and not b['2'] and not b['3'] and not b['4']:
            self.numbers_pressed.append(1)
        if not b['1'] and b['2'] and not b['3'] and not b['4']:
            self.numbers_pressed.append(2)
        if not b['1'] and not b['2'] and b['3'] and not b['4']:
            self.numbers_pressed.append(3)
        if not b['1'] and not b['2'] and not b['3'] and b['4']:
            self.numbers_pressed.append(4)
        
        # test the combination
        if self.numbers_pressed == self.PIN:
            # UNLOCK
            self.rainbow.set_all(0, 255, 0)
            self.rainbow.update()
            return
        
        if len(self.numbers_pressed) == 4:
            # 4 numbers entered, but it's not right
            self.attempts += 1
            self.rainbow.reset()
            if self.attempts >= 6:
                self.rainbow.set_all(255, 0, 0)
            else:
                for i in range(self.attempts):
                    self.rainbow.set_pixel(i, 255, 127, 0)
            self.rainbow.update()
            self.numbers_pressed = []
            
            
            
class MyProject(Project):
    required_modules = [SimpleCombinationLock,]
    
if __name__ == '__main__':
    MyProject()
    