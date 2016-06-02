from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Rainbow
from blackpearl.things import Slider


class DiscoLights(Module):
    listening_for = ['slider',]
    hardware_required = [Slider, Rainbow,]
    
    def receive(self, message):
        # We're listening for the slider, which gives us a value of between
        # 1 and 1000. We want to turn that into a value between 0 and 1, 
        # because that's what rainbow.hue() wants
        value = (message['slider']['value'])/1000.0
        # rainbow.hue() converts a value between 0 and 1 into r, g, b values
        red, green, blue = self.rainbow.hue(value)
        # Set all the lights on the rainbow to these values
        self.rainbow.set_all(red, green, blue)
        # Tell the rainbow to use those new values
        self.rainbow.update()


class MyProject(Project):
    modules_required = [DiscoLights, ]
    

if __name__ == '__main__':
    MyProject()