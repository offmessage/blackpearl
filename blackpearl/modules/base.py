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
    
    def __init__(self, project, hardware=None):
        self.project = project
        self.hardware = hardware


class SoftwareInput(Module):
    """An input module that is not related to a hardware module. Like a sine
    wave or a timer"""
    
    _flotilla_required = False
    
    def dispatch(self, data):
        self.data(data)
        
    def data(self, data):
        pass
    
        
class HardwareInput(Module):
    """An input module. Creates Input to the system, like the touch or dial"""
    
    _flotilla_required = True
    
    def dispatch(self, data):
        if self.hardware.module not in data:
            return
        self.data(data)
        
    def data(self, data):
        pass
    
        
class SoftwareOutput(Module):
    """An output module. Takes input and reacts to it in some way, like 
    printing to screen or calling a URL"""
    
    _flotilla_required = False


class HardwareOutput(Module):
    """An output module. Takes input and reacts to it in some way, like the
    motor or the number"""
    
    _flotilla_required = True


"""
    class BaseProject:
        
        def __init__(self, flotilla):
            self.flotilla = flotilla
            self._setModules()
            self._checkRequirements()
            
        def _setModules(self):
            \"""Create attributes on the instance for each connected module\"""
            modules = self.flotilla.modules
            connected = {}
            for channel in modules:
                module = modules[channel]
                if module is not None:
                    module_name = module.module
                    connected.setdefault(module_name, 0)
                    connected[module_name] += 1
                    name = '{}{}'.format(module_name, connected[module_name])
                    setattr(self, name, module)
                    
        def _checkRequirements(self):
            \"""Subclasses will define a requirements attribute for connected
            modules. This is either a list: ['motor', 'motor', 'slider'], or a
            dict: {0: 'motor', 1: 'motor', 2: 'slider'}\"""
            # XXX Check what numbering the channels are?
            if not hasattr(self, 'requirements'):
                # No requirements defined
                return
            
            if isinstance(self.requirements, list):
                reqs = Counter(self.requirements)
                mods = Counter(self.flotilla.modules.values())
                rem = mods - reqs
                if sum(rem.values()) == (sum(mods.values()) - sum(reqs.values())):
                    # All our requirements are met
                    return True
                print("Requirements not met")
                print("Requirements are:")
                for r in self.requirements:
                    print("   "+r)
                print("Connected modules are:")
                for m in self.flotilla.modules:
                    print("   {}: {}".format(m.channel, m.module))
                return False
            
            if isinstance(self.requirements, dict):
                for k in self.requirements:
                    if self.requirements[k] != self.flotilla.modules[k]:
                        return
                print("Requirements not met")
                print("Requirements are:")
                for r in self.requirements:
                    print("   {}: {}".format(r, self.requirements[r]))
                print("Connected modules are:")
                for m in self.flotilla.modules:
                    print("   {}: {}".format(m.channel, m.module))
                return False
            
        def _addModule(self, channel, module):
            self._checkRequirements()
        
        def _delModule(self, channel, module):
            self._checkRequirements()
        
        def update(self, channel, module, data):
            pass
        
        
    class TouchScroller(BaseProcessor):
        
        requirements = ['matrix', 'touch',]
        
        \"""when touch.button4 is pressed
        matrix.pause()
        when touch.button4 is released
        do nothing
        
        when touch.button1 is pressed
        add some text to the matrix
        matrix.scroll()\"""
    """
