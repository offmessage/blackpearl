"""
=======================================
Black Pearl: For twisted little pirates
=======================================

things/inputs/base.py

Communicate with the Flotilla hardware input modules.
"""

from ..base import FlotillaModule


class FlotillaInput(FlotillaModule):
    """
    Base class for input modules
    """
    
    def change(self, data):
        """Called when the Flotilla identifies an update from this module"""
        # Process the data as you see fit
        # Send it back to the flotilla class
        return self.broadcast(data)
        

class LinearInput(FlotillaInput):
    """
    Min value 0, Max value 1023. In reality it gets a bit fuzzy
    over 1018, and below 5, so we should probably cap out at those values
    """
    value = None
    
    def change(self, data):
        value = self.calculate(int(data))
        if self.value == value:
            # This might happen at the the upper and lower bounds
            return None
        self.value = value
        return self.broadcast({'value': value,})
    
    def calculate(self, value):
        # coping with the fuzziness around min and max values
        if value < 6:
            value = 0
        if value > 999:
            value = 1000
        return value


