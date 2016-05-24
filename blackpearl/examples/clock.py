from blackpearl.modules import Module
from blackpearl.modules import Clock
from blackpearl.projects import Project
from blackpearl.things import Number


class Listener(Module):
    listening_for = ['clock',]
    hardware_required = [Number,]
    
    def receive(self, message):
        tm = message['clock']['as_string']
        self.number.set_digit(0, tm[0])
        self.number.set_digit(1, tm[1])
        if tm[2] == ":":
            self.number.colon = 1
        else:
            self.number.colon = 0
        self.number.set_digit(2, tm[3])
        self.number.set_digit(3, tm[4])
        self.number.update()
        
        
class MyProject(Project):
    required_modules = [Clock, Listener,]
    

if __name__ == '__main__':
    MyProject()