from blackpearl.modules import Module
from blackpearl.projects import flotilla
from blackpearl.things import Rainbow
from blackpearl.things import Touch


class TouchTheRainbow(Module):
    listening_for = ['touch',]
    hardware_required = [Touch, Rainbow,]
    
    def receive(self, data):
        # We're listening for buttons!
        buttons = data['touch']['buttons']
        if buttons['1']:
            self.rainbow.set_all(255, 0, 0)
            self.rainbow.update()
        elif buttons['2']:
            self.rainbow.set_all(0, 255, 0)
            self.rainbow.update()
        elif buttons['3']:
            self.rainbow.set_all(0, 0, 255)
            self.rainbow.update()
        elif buttons['4']:
            self.rainbow.reset()


if __name__ == '__main__':
    flotilla.add_module(TouchTheRainbow)
    flotilla.run()
    