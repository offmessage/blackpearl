from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Colour
from blackpearl.things import Rainbow


class ColourMatcher(Module):
    hardware_required = [Colour, Rainbow,]
    listening_for = ['colour']
    
    def receive(self, message):
        colour = message['colour']['rgb']
        self.rainbow.reset()
        r = colour[0]
        g = colour[1]
        b = colour[2]
        self.rainbow.set_all(r, g, b)
        self.rainbow.update()
        

class MyProject(Project):
    modules_required = [ColourMatcher, ]
    

if __name__ == '__main__':
    MyProject()