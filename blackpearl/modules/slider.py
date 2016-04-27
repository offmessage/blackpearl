from .base import Module


class Slider(Module):
    
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
    

