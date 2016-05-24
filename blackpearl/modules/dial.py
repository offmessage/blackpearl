from .base import Module


class Dial(Module):
    
    module_name = 'dial'
    value = None
    
    def receive(self, message):
        value = message['value']
        if value != self.value:
            self.value_changed(value)
            self.value = value
            
    def value_changed(self, value):
        pass
    
    
