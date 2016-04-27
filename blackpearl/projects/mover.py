from blackpearl.modules import BaseModule
from blackpearl.projects import BaseProject


class Mover(BaseModule):
    listening_for = ['slider',]
    hardware_required = ['slider', 'motor', 'motor',]
    
    def data(self, data):
        value = data['slider']['value']
        if value == 0:
            v = -63
        elif value == 1000:
            v = 63
        else:
            v = int((value - 500)/8)
        
        self.motor1.set_speed(v)
        self.motor2.set_speed(v * -1)


class Project(BaseProject):
    required_modules = [Mover,]
    

if __name__ == '__main__':
    Project()