from blackpearl.modules import BaseModule
from blackpearl.modules import Timer
from blackpearl.projects import Project


class MyTimer(Timer):
    tick = 0.1
    def setup(self):
        self.start()
        
class Listener(BaseModule):
    listening_for = ['timer']
    def receive(self, data):
        print(data['timer']['time'])
        
class MyProject(Project):
    required_modules = [MyTimer, Listener,]
    

if __name__ == '__main__':
    MyProject()