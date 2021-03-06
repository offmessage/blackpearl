from decimal import Decimal
import time

from twisted.internet import defer
from twisted.internet import reactor

from .base import Module

# XXX Arguably to give this same API (module.timer.stop() etc) this
# needs changing, with a secondary class having all the controls

class Timer(Module):
    
    module_name = 'timer'
    status = 'STOPPED'
    tick = 0.01 # how frequently should the timer tick (in seconds)
    precision = '' # Can be a string suitable for decimal.Decimal.quantize()
    tick_count = 0
    
    def __init__(self, project):
        if self.tick < 0.01:
            msg = ("Setting `tick` of a timer to less than 1/100th of a second "
                   "is likely to impact the performance of other modules "
                   "connected to your Flotilla. Doesn't mean you can't try "
                   "though!")
            project.log('WARNING', msg)
        super().__init__(project)
        self.setup()
        
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
        self.broadcast(data)
        
    @defer.deferredGenerator
    def start(self):
        self.status = "RUNNING"
        while self.status == "RUNNING":
            if self.status != "RUNNING":
                # we are paused or stopped
                break
            d = defer.Deferred()
            self.update()
            reactor.callLater(self.tick, d.callback, None)
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
    
    
class Clock(Timer):
    
    module_name = 'clock'
    tick = 0.5
    colon = True
    
    def setup(self):
        self.start_time = time.time()
        self.start()
        
    def update(self):
        tm = time.localtime(time.time())
        if self.colon:
            fmt = "{:02d}:{:02d}"
        else:
            fmt = "{:02d} {:02d}"
        self.colon = not self.colon
        data = {'hours': "{:02d}".format(tm.tm_hour),
                'mins': "{:02d}".format(tm.tm_min),
                'seconds': "{:02d}".format(tm.tm_sec),
                'as_string': fmt.format(tm.tm_hour, tm.tm_min),
                }
        self.broadcast(data)
        