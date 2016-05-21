from blackpearl.modules import Module
from blackpearl.projects import Project


class DiscoLights(Module):
    listening_for = ['slider',]
    hardware_required = ['slider', 'rainbow',]
    
    def receive(self, data):
        # We're listening for the slider, which gives us a value of between
        # 1 and 1000. We want to turn that into a value between 0 and 1, 
        # because that's what rainbow.hue() wants
        value = (data['slider']['value'])/1000.0
        # rainbow.hue() converts a value between 0 and 1 into r, g, b values
        red, green, blue = self.rainbow.hue(value)
        # Set all the lights on the rainbow to these values
        self.rainbow.set_all(red, green, blue)
        # Tell the rainbow to use those new values
        self.rainbow.update()


class MyProject(Project):
    required_modules = [DiscoLights, ]
    

if __name__ == '__main__':
    MyProject()