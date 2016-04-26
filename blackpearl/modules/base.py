"""
=======================================
Black Pearl: For twisted little pirates
=======================================

modules/base.py

Base classes for our modules.
"""


from collections import Counter


class Module:
    
    module_name = None
    listening_for = []
    
    def __init__(self, project, hardware=None):
        self.project = project
        self.hardware = hardware
        if self._flotilla_required:
            self.project.requireFlotilla()


class Input:
    
    def dispatch(self, data):
        for l in self.listening_for:
            if l not in data:
                return
        self.data(data)
        
    def data(self, data):
        pass
    

class Output:
    pass


class Software:
    
    _flotilla_required = False
    
    
class Hardware:
    
    _flotilla_required = True
    
    
class SoftwareInput(Module, Software, Input):
    """An input module that is not related to a hardware module. Like a sine
    wave or a timer"""
    
        
class HardwareInput(Module, Hardware, Input):
    """An input module. Creates Input to the system, like the touch or dial"""
    
        
class SoftwareOutput(Module, Software, Output):
    """An output module. Takes input and reacts to it in some way, like 
    printing to screen or calling a URL"""
    

class HardwareOutput(Module, Hardware, Output):
    """An output module. Takes input and reacts to it in some way, like the
    motor or the number"""
    

