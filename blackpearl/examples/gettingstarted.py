from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Rainbow
from blackpearl.things import Touch


class TouchTheRainbow(Module):
    listening_for = ['touch',]
    hardware_required = [Touch, Rainbow,]
    
    def receive(self, message):
        # We're listening for buttons!
        buttons = message['touch']['buttons']
        if buttons['1'] is True:
            self.rainbow.set_all(255, 0, 0)
            self.rainbow.update()
        elif buttons['2'] is True:
            self.rainbow.set_all(0, 255, 0)
            self.rainbow.update()
        elif buttons['3'] is True:
            self.rainbow.set_all(0, 0, 255)
            self.rainbow.update()
        elif buttons['4'] is True:
            self.rainbow.reset()


class MyProject(Project):
    modules_required = [TouchTheRainbow,]
    
    
if __name__ == '__main__':
    MyProject()
    