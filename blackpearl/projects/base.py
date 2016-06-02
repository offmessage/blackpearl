"""
=======================================
Black Pearl: For twisted little pirates
=======================================

projects/base.py

The base for our own projects.
"""

import time

from decimal import Decimal
# Shim for the fact that gcd moves to math in Python 3.5
import math
try:
    GCD = math.gcd
except AttributeError:
    import fractions
    GCD = fractions.gcd
import functools

from twisted.internet import defer
from twisted.internet import reactor

from ..things import FlotillaClient


class BaseProject:
    
    modules_required = []
    flotilla = None
    
    def __init__(self, flotilla_port="/dev/ttyACM0", baudrate=115200):
        self.modules = []
        self._listened_for = []
        self._flotilla_port = flotilla_port
        self._baudrate = baudrate
        self._running = False
        self._time_subscribers = {}
        
    def run(self):
        self.flotilla = FlotillaClient()
        self.flotilla.run(self, reactor)
        reactor.run()
        self._running = True
    
    def add_module(self, klass):
        if self._running:
            self.log("ERROR", "Cannot add new modules to an already running project")
            return
        self.modules_required.append(klass)
        
    def connectModules(self):
        # This is called by the flotilla once the hardware is all available
        project = self
        self.modules = [ k(project) for k in self.required_modules ]
        listened_for = []
        for m in self.modules:
            listened_for.extend(m.listening_for)
            if m._ticks:
                for k, v in m._ticks.items():
                    if k in self._time_subscribers:
                        self._time_subscribers[k].extend(v)
                    else:
                        self._time_subscribers[k] = v
        self._listened_for = list(set(listened_for))
        if self._time_subscribers:
            # We need to set up a clock able to fire for everyone
            tick_rates = list(map(lambda x: x*10000, self._time_subscribers.keys()))
            if len(tick_rates) == 1:
                # Simple case
                self._tick_rate = tick_rates[0]/10000
            elif len(tick_rates) == 2:
                self._tick_rate = GCD(*tick_rates)/10000
            else:
                self._tick_rate = functools.reduce(GCD, tick_rates)/10000
            
    def all_connected(self, module):
        # Gets called once for every module connected. If only one is hardware
        # the ``check`` will be True multiple times. We only want to call
        # ``_start_clock()`` once.
        check = all([ mod._all_connected for mod in self.modules ])
        if check and self._time_subscribers and not getattr(self, '_clock_running', False):
            self._start_clock()
            
    @defer.deferredGenerator
    def _start_clock(self):
        self._clock_running = True
        self._time = 0
        
        def mod_by_zero(a, b):
            # a % b raises DividedByZero if b is 0. But we want everyone to
            # get called with the first 0, so we need our own function
            if b == 0:
                return 0
            return a % b
        
        def ticker(tm):
            # Gets called with every tick, only calls those that are listening
            # for this particular tick count
            for k in self._time_subscribers:
                if mod_by_zero(int(tm * 10000), int(k * 10000)) == 0:
                    for sub in self._time_subscribers[k]:
                        sub.tick(tm)
        
        while True:
            d = defer.Deferred()
            #d.addCallback(ticker)
            ticker(self._time)
            reactor.callLater(self._tick_rate, d.callback, None)
            wfd = defer.waitForDeferred(d)
            self._time += self._tick_rate
            self._time = float(Decimal(self._time).quantize(Decimal(str(self._tick_rate))))            
            yield wfd
    
    def connect(self):
        # Called if a new piece of hardware is connected to the Flotilla
        for m in self.modules:
            m._checkRequirements()
            
    def message(self, data):
        if data is None:
            return
        for module in self.modules:
            module.dispatch(data)
            
    def log(self, level, message):
        if 'log' in self._listened_for:
            data = {'log': {'level': level,
                            'message': message,
                            }
                    }
            self.message(data)
        else:
            print(level, ":", message)

        
class Project(BaseProject):
    
    def __init__(self, flotilla_port="/dev/ttyACM0", baudrate=115200):
        super().__init__(flotilla_port, baudrate)
        self.run()
        
    