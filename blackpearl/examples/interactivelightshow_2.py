from blackpearl.modules import Module
from blackpearl.projects import Project
from blackpearl.things import Rainbow
from blackpearl.things import Touch


class TouchTheRainbow(Module):
    listening_for = ['touch',]
    hardware_required = [Touch, Rainbow,]
    
    button1_press_count = 0
    button2_press_count = 0
    colours = [(255,51,204),
               (255,102,51),
               (204,255,51),
               (204,51,255),
               (102,51,255),
               (102,255,51),
               (51,102,255),
               (255,204,51),
               (51,255,102),
               ]
    
    def update_rainbow(self):
        colour_index = self.button1_press_count % len(self.colours)
        r, g, b = self.colours[colour_index]
        
        active_pixel = self.button2_press_count % 5
        
        self.rainbow.reset()
        self.rainbow.set_pixel(active_pixel, r, g, b)
        self.rainbow.update()
        
    def receive(self, message):
        buttons = message['touch']['buttons']
        if buttons['1'] is True:
            self.button1_press_count += 1
            self.update_rainbow()
        if buttons['2'] is True:
            self.button2_press_count += 1
            self.update_rainbow()

    def setup(self):
        self.update_rainbow()
        

class MyProject(Project):
    modules_required = [TouchTheRainbow,]
    
    
if __name__ == '__main__':
    MyProject()
    