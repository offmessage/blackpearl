from blackpearl.modules import BaseModule
from blackpearl.projects import BaseProject


class Colour(BaseModule):
    hardware_required = ['colour', 'rainbow',]
    listening_for = ['colour']
    
    def receive(self, data):
        r, g, b = data['colour']['rgb']
        print(r, g, b)
        #self.rainbow.set_all(r, g, b)
        #self.rainbow.update()
        
class Project(BaseProject):
    required_modules = [Colour,]
    

if __name__ == '__main__':
    Project()