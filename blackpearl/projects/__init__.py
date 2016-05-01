"""
=======================================
Black Pearl: For twisted little pirates
=======================================

projects/

The base for our own projects.
"""


from twisted.internet import reactor

from blackpearl.hardware import FlotillaClient


class BaseProject:
    
    required_modules = []
    flotilla = None
    
    def __init__(self, flotilla_port="/dev/ttyACM0", baudrate=115200):
        self.modules = []
        self._flotilla_port = flotilla_port
        self._baudrate = baudrate
        self.flotilla = FlotillaClient()
        self.flotilla.run(self, reactor)
        reactor.run()
    
    def connectModules(self):
        project = self
        self.modules = [ k(project) for k in self.required_modules ]
    
    def connect(self):
        for m in self.modules:
            m._checkRequirements()
            
    def message(self, data):
        if data is None:
            return
        for module in self.modules:
            module.dispatch(data)
            
    def log(self, level, message):
        # XXX replace this with something prettier
        print(level, ":", message)
        
