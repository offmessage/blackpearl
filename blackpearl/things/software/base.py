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
            self._module.project.log('WARNING', msg)
        if self.tick_rate < 0.0001:
            raise ValueError("Can't cope with a tick rate below 0.0001")
        
    def tick(self, tm):
        # Override this with whatever you want to happen every tick
        data = {'status': self.status,
                'time': tm,
                }
        self.broadcast(data)
            
        
class TimeBasedUnsynced(SoftwareModule):
    
    sync = False
    time = 0
    auto_start = True
    status = "STOPPED"
    
    def __init__(self, module):
        super().__init__(module)
        if self.auto_start:
            self.start()
        
    def tick(self, tm):
        # Override this with whatever you want to happen every tick
        data = {'status': self.status,
                'time': tm,
                }
        self.broadcast(data)
            
    def check(self):
        return self.status == "RUNNING"
    
    @defer.deferredGenerator
    def start(self):
        """Define our own clock"""
        self.status = "RUNNING"
        while self.check():
            d = defer.Deferred()
            self.tick(self.time)
            reactor.callLater(self.tick_rate, d.callback, None)
            wfd = defer.waitForDeferred(d)
            self.time += self.tick_rate
            self.time = float(Decimal(self.time).quantize(Decimal(str(self.tick_rate))))            
            yield wfd
        self.timer_stopped()
    
    def timer_stopped(self):
        pass
    
    def reset(self):
        self.status = 'STOPPED'
        self.time = 0
    
    def stop(self):
        self.status = 'STOPPED'
        
    def pause(self):
        if self.status == 'RUNNING':
            self.status = 'PAUSED'
        elif self.status == 'PAUSED':
            self.start()

        
