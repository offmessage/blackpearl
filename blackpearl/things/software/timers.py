import time

from .base import TimeBased
from .base import TimeBasedUnsynced


class Countdown(TimeBasedUnsynced):
    
    module = 'countdown'
    time = 10
    tick_rate = -0.01
    auto_start = False
    
    def check(self):
        return self.status == "RUNNING" and self.time > 0
    
    def timer_stopped(self):
        if self.time == 0:
            self.status = "STOPPED"
            data = {'status': 'COMPLETED',
                    'time': self.time,
                    }
            self.broadcast(data)
            
class Stopwatch(TimeBasedUnsynced):
    
    module = 'stopwatch'
    tick_rate = 0.01
    auto_start = False
    
    
class Clock(TimeBased):
    
    module = 'clock'
    tick_rate = 0.5
    auto_start = True
    colon = True
    
    def tick(self, tm):
        # ignore the time sent by the tick - instead get localtime
        tm = time.localtime(time.time())
        
        if self.colon:
            fmt = "{:02d}:{:02d}"
        else:
            fmt = "{:02d} {:02d}"
        self.colon = not self.colon
        
        data = {'status': 'RUNNING',
                'hours': "{:02d}".format(tm.tm_hour),
                'minutes': "{:02d}".format(tm.tm_min),
                'seconds': "{:02d}".format(tm.tm_sec),
                'colon': self.colon,
                'as_string': fmt.format(tm.tm_hour, tm.tm_min),
                }
        self.broadcast(data)
