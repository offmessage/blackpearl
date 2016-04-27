from .base import BaseModule


class Slider(BaseModule):
    
    module_name = 'slider'
    listening_for = ['slider',]
    value = None
    
    def data(self, data):
        value = data['value']
        if value != self.value:
            self.value_changed(value)
            self.value = value
            
    def value_changed(self, value):
        pass
    

