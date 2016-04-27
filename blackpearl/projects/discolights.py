from blackpearl.modules import BaseModule
from blackpearl.projects import BaseProject


class DiscoLights(BaseModule):
    listening_for = ['slider',]
    hardware_required = ['slider', 'rainbow',]
    
    def data(self, data):
        value = (data['slider']['value'])/1000.0
        red, green, blue = self.rainbow.hue(value)
        self.rainbow.set_all(red, green, blue)
        self.rainbow.update()


class Project(BaseProject):
    required_modules = [DiscoLights, ]
    

if __name__ == '__main__':
    Project()