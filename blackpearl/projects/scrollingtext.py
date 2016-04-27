from blackpearl.modules import Touch
from blackpearl.projects import BaseProject


class Scroller(Touch):
    listening_for = ['touch',]
    hardware_required = ['touch', 'matrix',]
    
    def button1_pressed(self):
        self.matrix.addText("This is a great example!")
        self.matrix.scrollspeed = 2
        self.matrix.loop = True
        self.matrix.scroll()
        

class Project(BaseProject):
    required_modules = [Scroller, ]
    

if __name__ == '__main__':
    Project()