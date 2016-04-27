from decimal import Decimal
import time

from twisted.internet import defer
from twisted.internet import reactor

from .base import BaseModule

# XXX Arguably to give this same API (module.timer.stop() etc) this
# needs changing, with a secondary class having all the 

class Timer(BaseModule):
    
    module_name = 'timer'
    status = 'STOPPED'
    tick = 1 # how frequently should the timer tick (in seconds)
    precision = '' # Can be a string suitable for decimal.Decimal.quantize()
    tick_count = 0
    
    def setup(self):
        # This is run when the class is instantiated, so you could start
        # the timer here if you wanted, by uncommenting the following
        #self.start()
        pass
        
    def update(self):
        # Emit the new time to someone that's listening
        self.tick_count += 1
        newtime = self.tick * self.tick_count
        # Sometimes we will get microseconds appended due to clock timings
        # This strips them
        if self.precision == '':
            if self.tick >= 1:
                self.precision = '1.'
            else:
                self.precision = str(self.tick)
        newtime = float(Decimal(newtime).quantize(Decimal(self.precision)))
        data = {'time': newtime}
        self.emit(data)
        
    @defer.deferredGenerator
    def start(self):
        self.status = "RUNNING"
        while self.status == "RUNNING":
            if self.status != "RUNNING":
                # we are paused or stopped
                break
            d = defer.Deferred()
            reactor.callLater(self.tick, d.callback, self.update())
            wfd = defer.waitForDeferred(d)
            yield wfd
    
    def reset(self):
        self.status = 'STOPPED'
        self.tick_count = 0
    
    def stop(self):
        self.status = 'STOPPED'
        
    def pause(self):
        if self.status == 'RUNNING':
            self.status = 'PAUSED'
        elif self.status == 'PAUSED':
            self.start()
        pass
    
    