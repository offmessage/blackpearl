from decimal import Decimal

from twisted.internet import defer
from twisted.internet import reactor

class SoftwareModule:
    
    module = ''
    
    def __init__(self, module):
        self._module = module
        if not self.module:
            raise ValueError("Must set a module name")
        
    def log(self, level, message):
        self._module.project.log(level, message)
        
    def broadcast(self, data):
        output = {self.module: data}
        self._module.project.message(output)
        

class TimeBased(SoftwareModule):
    
    sync = True
    tick_rate = None
    
    def __init__(self, module):
        super().__init__(module)
        if self.tick_rate is None:
            raise ValueError("Must set a tick_rate for a time based module")
        if 0.0001 < self.tick_rate < 0.01:
            msg = ("Setting `tick` of a timer to less than 1/100th of a second "
                   "is likely to impact the performance of other modules "
                   "connected to your Flotilla. Doesn't mean you can't try "
                   "though!")
            project.log('WARNING', msg)
        if self.tick_rate < 0.0001:
            raise ValueError("Can't cope with a tick rate below 0.0001")
        
    def tick(self, tm):
        # gets called with the new time every tick, frequency set by
        # self.tick_rate
        pass
    
        
class TimeBasedUnsynced(SoftwareModule):
    # XXX TODO: Provide start, stop and pause methods, otherwise why unsync?
    sync = False
    time = 0
    
    def __init__(self, module):
        super().__init__(module)
        self.start()
        
    @defer.deferredGenerator
    def start(self):
        """Define our own clock"""
        while True:
            d = defer.Deferred()
            d.addCallback(self.tick)
            reactor.callLater(self.tick_rate, d.callback, self.time)
            wfd = defer.waitForDeferred(d)
            self.time += self.tick_rate
            self.time = float(Decimal(self.time).quantize(Decimal(str(self.tick_rate))))            
            yield wfd
    

        