from twisted.internet import reactor
from twisted.internet.serialport import SerialPort

from blackpearl.client import FlotillaClient

class Recipe:
    
    def __init__(self):
        # Do lots of things
        # ...
        #
        flotilla = FlotillaClient()
        SerialPort(flotilla, '/dev/ttyACM0', reactor, baudrate=115200)
        reactor.run()
        
class BaseProcessor:
    
    def __init__(self, flotilla):
        self.flotilla = flotilla
        
    def addModule(self, channel, module):
        pass
    
    def delModule(self, channel, module):
        pass
    
    def update(self, channel, module, data):
        pass