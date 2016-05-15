from .base import BaseModule


class Dial(BaseModule):
    
    module_name = 'dial'
    value = None
    
    def receive(self, data):
        value = data['value']
        if value != self.value:
            self.value_changed(value)
            self.value = value
            
    def value_changed(self, value):
        pass
    
    
