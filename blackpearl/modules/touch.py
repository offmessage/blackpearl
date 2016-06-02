from .base import Module
from ..things import Touch


class Touch(Module):
    
    listening_for = ['touch']
    hardware_required = [Touch,]

    module_name = 'touch_module' # icky, but it can't have the same name as the
                                 # hardwar itself
                                 
    buttons = {'1': False,
               '2': False,
               '3': False,
               '4': False,
               }

    def receive(self, message):
        buttons = message['touch']['buttons']
        for k in buttons:
            method_name = None
            if not self.buttons[k] and buttons[k]:
                # Button k has been pressed
                method_name = 'button{}_pressed'.format(k)
                self.buttons[k] = True
            if self.buttons[k] and not buttons[k]:
                # Button k has been released
                method_name = 'button{}_released'.format(k)
                self.buttons[k] = False
            if method_name is not None:
                method = getattr(self, method_name, None)
                if method is not None:
                    method()
                    
    def button1_pressed(self):
        pass
    
    def button1_released(self):
        pass
    
    def button2_pressed(self):
        pass
    
    def button2_released(self):
        pass
    
    def button3_pressed(self):
        pass
    
    def button3_released(self):
        pass
    
    def button4_pressed(self):
        pass
    
    def button4_released(self):
        pass
    

