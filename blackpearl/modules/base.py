from zope.interface import Interface
from zope.interface import implements


class IFlotillaModule:
    module = "The module name"
    
class IFlotillaInput:
    def change(data):
        """
        Accept a data update from the Flotilla Client, return None if no change,
        a dict if there is a change
        """
        
class IFlotillaOutput:
    def send(channel, data):
        """
        Send an update to the Flotilla Client for the matching output device
        """
        
class FlotillaModule:
    
    implements(IFlotillaModule)
    
    def __init__(self, flotilla, channel):
        self.flotilla = flotilla
        self.channel = channel
        
        
class FlotillaInput(FlotillaModule):
    """
    Base class for input modules
    """
    
    implements(IFlotillaInput)
    
    def change(self, data):
        """Called when the Flotilla identifies an update from this module"""
        print(data)


class LinearInput(FlotillaInput):
    """
    Min value 0, Max value 1023. In reality it gets a bit fuzzy
    over 1018, and below 5, so we should probably cap out at those values
    """
    VALUE = None
    
    def change(self, data):
        value = int(data)
        if self.VALUE == value:
            # This will never happen, unlike the Touch
            return None
        self.VALUE = value
        return {'value': value,}
    
    
class FlotillaOutput(FlotillaModule):
    """
    Base class for output modules
    """
    
    implements(IFlotillaOutput)
    
    def send(self, data):
        """One should perform validation on the data here"""
        #num = ["0"]*8
        #num.append("40")
        #data = ",".join(num)
        self.flotilla.flotillaCommand(self.channel, data)


    
