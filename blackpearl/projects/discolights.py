from blackpearl.modules.base import BaseModule
from blackpearl.projects import BaseProject


class DiscoLights(BaseModule):
    listening_for = ['dial', 'slider',]
    hardware_required = ['dial', 'slider', 'rainbow']
    
    slider_value = 0
    dial_value = 0
    
    def data(self, data):
        if 'slider' in data:
            value1 = (data['slider']['value'])/1000.0
            value2 = self.dial_value
            self.slider_value = value1
        elif 'dial' in data:
            value1 = self.slider_value
            value2 = (data['dial']['value'])/1000.0
            self.dial_value = value2
        value = (value1 + value2)/2.0
        hue = self.rainbow.hue(value)
        self.rainbow.set_all(*hue)
        self.rainbow.update()


class Project(BaseProject):
    required_modules = [DiscoLights, ]
    

if __name__ == '__main__':
    Project()