from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Colour
from blackpearl.things import Rainbow


class ColourMatcher(Module):
    hardware_required = [Colour, Rainbow,]
    listening_for = ['colour']
    
    def receive(self, message):
        rgb = message['colour']['rgb']
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        self.rainbow.set_all(r, g, b)
        self.rainbow.update()
        

class MyProject(Project):
    required_modules = [ColourMatcher, ]
    

if __name__ == '__main__':
    MyProject()