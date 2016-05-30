from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Number
from blackpearl.things import Clock

import time

class KitchenClock(Module):
    
    hardware_required = [Number,]
    software_required = [Clock,]
    listening_for = ['clock',]
    
    def receive(self, message):
        hours = message['clock']['hours']
        minutes = message['clock']['minutes']
        colon = message['clock']['colon']
        digits = hours + minutes # not a string of length 4
        for c, digit in enumerate(digits):
            self.number.set_digit(c, digit)
        self.number.colon = colon
        self.number.update()
        
        
class MyProject(Project):
    required_modules = [KitchenClock,]
    
if __name__ == '__main__':
    MyProject()
    
