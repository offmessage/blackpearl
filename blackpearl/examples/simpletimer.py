from blackpearl.modules import Module
from blackpearl.modules import Timer
from blackpearl.projects import Project


class MyTimer(Timer):
    tick = 0.1
    def setup(self):
        self.start()
        
class Listener(Module):
    listening_for = ['timer']
    def receive(self, message):
        print(message['timer']['time'])
        
class MyProject(Project):
    required_modules = [MyTimer, Listener,]
    

if __name__ == '__main__':
    MyProject()