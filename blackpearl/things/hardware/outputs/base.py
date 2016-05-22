"""
=======================================
Black Pearl: For twisted little pirates
=======================================

things/outputs/base.py

Communicate with the Flotilla hardware output modules.
"""


from ..base import FlotillaModule


class FlotillaOutput(FlotillaModule):
    """
    Base class for output modules
    """
    
    def send(self, data):
        datastring = ','.join([ str(d) for d in data ])
        cmd = "s {} {}".format(self.channel, datastring).encode()
        self.flotilla.flotillaCommand(cmd)
        
