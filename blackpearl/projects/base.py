"""
=======================================
Black Pearl: For twisted little pirates
=======================================

projects/base.py

The base for our own projects.
"""


from twisted.internet import reactor

from blackpearl.hardware import FlotillaClient


class BaseProject:
    
    required_modules = []
    flotilla = None
    
    def __init__(self, flotilla_port="/dev/ttyACM0", baudrate=115200):
        self.modules = []
        self._listened_for = []
        self._flotilla_port = flotilla_port
        self._baudrate = baudrate
        self._running = False
        
    def run(self):
        self.flotilla = FlotillaClient()
        self.flotilla.run(self, reactor)
        reactor.run()
        self._running = True
    
    def add_module(self, klass):
        if self._running:
            self.log("ERROR", "Cannot add new modules to an already running project")
            return
        self.required_modules.append(klass)
        
    def connectModules(self):
        # This is called by the flotilla once the hardware is all available
        project = self
        self.modules = [ k(project) for k in self.required_modules ]
        listened_for = []
        for m in self.modules:
            listened_for.extend(m.listening_for)
        self._listened_for = list(set(listened_for))
    
    def connect(self):
        # Called if a new piece of hardware is connected to the Flotilla
        for m in self.modules:
            m._checkRequirements()
            
    def message(self, data):
        if data is None:
            return
        for module in self.modules:
            module.dispatch(data)
            
    def log(self, level, message):
        if 'log' in self._listened_for:
            data = {'log': {'level': level,
                            'message': message,
                            }
                    }
            self.message(data)
        else:
            print(level, ":", message)

        
class Project(BaseProject):
    
    def __init__(self, flotilla_port="/dev/ttyACM0", baudrate=115200):
        super().__init__(flotilla_port, baudrate)
        self.run()
        
    