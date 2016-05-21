from blackpearl.modules import BaseModule
from blackpearl.projects import Project


class Mover(BaseModule):
    listening_for = ['slider',]
    hardware_required = ['slider', 'motor', 'motor',]
    
    def receive(self, data):
        value = data['slider']['value'] # This is between 0 and 1000
        if value == 0:
            # if value is 0 then we want maximum reverse speed!
            v = -63
        elif value == 1000:
            # if value is 1000 then we want maximum forward speed!
            v = 63
        else:
            # otherwise take 500 off value (so now value is between -500 and +500
            # and then divide by 8 (so now it's between -63 and 63) and finally
            # put it through int() so that we knock off the decimal points (by
            # making it an integer)
            v = int((value - 500)/8)
        
        self.motor1.set_speed(v)
        self.motor2.set_speed(v * -1)


class MyProject(Project):
    required_modules = [Mover,]
    

if __name__ == '__main__':
    MyProject()