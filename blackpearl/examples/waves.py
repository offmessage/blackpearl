from blackpearl.modules import Module
from blackpearl.projects import flotilla
from blackpearl.things import Number
from blackpearl.things import Rainbow
from blackpearl.things import Sine


class Listener(Module):
    
    hardware_required = [Number,]
    software_required = [Sine,]
    listening_for = ['sinewave',]
    
    def receive(self, message):
        self.project.log("INFO", message)
        v = message['sinewave']['value']
        if v < -0.6:
            active = 0
        elif v < -0.2:
            active = 1
        elif v < 0.2:
            active = 2
        elif v < 0.6:
            active = 3
        else:
            active = 4
        #for i in range(5):
            #if i != active:
                #self.rainbow.set_pixel(i, 0, 0, 0)
            #else:
                #self.rainbow.set_pixel(i, 255, 0, 0)
        #self.rainbow.update()
        self.number.set_number(active)
        self.number.update()
        
if __name__ == '__main__':
    flotilla.add_module(Listener)
    flotilla.run()