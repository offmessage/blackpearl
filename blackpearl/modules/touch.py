from .base import HardwareInput


class Touch(HardwareInput):
    
    module_name = 'touch'
    buttons = {1: False,
                2: False,
                3: False,
                4: False,
                }

    def data(self, data):
        buttons = data['buttons']
        for k in buttons:
            method_name = None
            if not self.buttons[k] and buttons[k]:
                # Button k has been pressed
                method_name = 'button{}_pressed'.format(k)
            if self.buttons[k] and not buttons[k]:
                # Button k has been released
                method_name = 'button{}_released'.format(k)
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
    

