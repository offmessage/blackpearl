"""
=======================================
Black Pearl: For twisted little pirates
=======================================

hardware/base.py

Base class for communicating with Flotilla hardware modules.
"""


class FlotillaModule:
    
    def __init__(self, flotilla, channel):
        self.flotilla = flotilla
        self.channel = channel
        
    def broadcast(self, data):
        if data is None:
            return data
        data['channel'] = self.channel
        output = {self.module: data}
        self.flotilla.message(output)


