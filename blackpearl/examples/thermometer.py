from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Rainbow
from blackpearl.things import Weather


class Thermometer(Module):
    listening_for = ['weather',]
    hardware_required = [Weather, Rainbow,]
    
    cold = (0, 0, 255)
    warm = (255, 128, 0)
    hot = (255, 0, 0)

    def receive(self, message):
        temperature = message['weather']['temperature']
        
        if temperature < 16:
            colour = self.cold
            leds = [0,]
        elif temperature < 17:
            colour = self.warm
            leds = [0,]
        elif temperature < 18:
            colour = self.warm
            leds = [0, 1,]
        elif temperature < 19:
            colour = self.warm
            leds = [0, 1, 2,]
        elif temperature < 20:
            colour = self.warm
            leds = [0, 1, 2, 3,]
        elif temperature < 21:
            colour = self.warm
            leds = [0, 1, 2, 3, 4,]
        else:
            colour = self.hot
            leds = [0, 1, 2, 3, 4,]
        
        self.rainbow.reset()
        r = colour[0]
        g = colour[1]
        b = colour[2]
        for led in leds:
            self.rainbow.set_pixel(led, r, g, b)
        self.rainbow.update()
        

class MyProject(Project):
    required_modules = [Thermometer,]
    
    
if __name__ == '__main__':
    MyProject()
    