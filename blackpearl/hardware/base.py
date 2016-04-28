"""
=======================================
Black Pearl: For twisted little pirates
=======================================

hardware/base.py

Communicate with the Flotilla hardware modules.
"""


class FlotillaModule:
    
    def __init__(self, flotilla, channel):
        self.flotilla = flotilla
        self.channel = channel
        
    def emit(self, data):
        if data is None:
            return data
        output = {self.module: data}
        self.flotilla.message(output)


class FlotillaInput(FlotillaModule):
    """
    Base class for input modules
    """
    
    def change(self, data):
        """Called when the Flotilla identifies an update from this module"""
        # Process the data as you see fit
        # Send it back to the flotilla class
        return self.emit(data)
        

class LinearInput(FlotillaInput):
    """
    Min value 0, Max value 1023. In reality it gets a bit fuzzy
    over 1018, and below 5, so we should probably cap out at those values
    """
    VALUE = None # XXX mixed use of capitalisation for this type of attribute
    
    def change(self, data):
        value = self.calculate(int(data))
        if self.VALUE == value:
            # This might happen at the the upper and lower bounds
            return None
        self.VALUE = value
        return self.emit({'value': value,})
    
    def calculate(self, value):
        # coping with the fuzziness around min and max values
        if value < 6:
            value = 0
        if value > 999:
            value = 1000
        return value


class FlotillaOutput(FlotillaModule):
    """
    Base class for output modules
    """
    
    def send(self, data):
        datastring = ','.join([ str(d) for d in data ])
        cmd = "s {} {}".format(self.channel, datastring).encode()
        self.flotilla.flotillaCommand(cmd)


    
