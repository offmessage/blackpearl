"""
==============
FlotillaClient
==============

This is the core Python code for connecting to, processing input from, and
sending messages to the Flotilla itself.

"""


from serial import SerialException

from twisted.internet import defer
from twisted.internet.serialport import SerialPort
from twisted.protocols.basic import LineReceiver

from .hardware import Colour
from .hardware import Dial
from .hardware import Joystick
from .hardware import Light
from .hardware import Matrix
from .hardware import Motion
from .hardware import Motor
from .hardware import Number
from .hardware import Rainbow
from .hardware import Slider
from .hardware import Touch
from .hardware import Weather


class FlotillaClient(LineReceiver):
    
    MODULES = {'matrix': Matrix,
               'number': Number,
               'rainbow': Rainbow,
               'motor': Motor,
               'touch': Touch,
               'dial': Dial,
               'slider': Slider,
               'joystick': Joystick,
               'motion': Motion,
               'light': Light,
               'colour': Colour,
               'weather': Weather,
               }
    
    def _resetModules(self):
        self.modules = { x: None for x in range(1, 9) }
        
    def run(self, project, reactor):
        self.project = project
        self.reactor = reactor
        self._ready = False
        self._connected = False
        flotilla_port = self.project._flotilla_port
        baudrate = self.project._baudrate
        try:
            SerialPort(self, flotilla_port, reactor, baudrate)
        except SerialException as e:
            if not hasattr(self, '_count'):
                self._count = 0
            print("Trying to connect to Flotilla. This may take up to 30 seconds")
            self._count += 1
            if self._count <= 30:
                if self._count % 5 == 0:
                    print("Trying... {} seconds".format(self._count))
                def runner(arg):
                    self.run(project, reactor)
                d = defer.Deferred()
                d.addCallback(runner)
                reactor.callLater(1, d.callback, None)
                return defer.waitForDeferred(d)
            else:
                # It took more than 30 seconds (I've never seen this)
                raise e
        
    def connectionLost(self, reason):
        self._resetModules()
        print('Flotilla is disconnected.')
        
    @defer.deferredGenerator
    def connectionMade(self):
        self._resetModules()
        self._lines = []
        print('Flotilla is connected.')
        self.flotillaCommand(b'v')
        def check(arg):
            self.flotillaCommand(b'v')
        while not self._ready:
            d = defer.Deferred()
            d.addCallback(check)
            self.reactor.callLater(1, d.callback, None)
            wfd = defer.waitForDeferred(d)
            yield wfd
        
    def flotillaCommand(self, cmd):
        self.delimiter = b'\r'
        self.sendLine(cmd)
        self.delimiter = b'\r\n'
        
    def handle_hash(self, line):
        
        self.project.log("INFO", line)
        
        if self._ready:
            # We are all good. No action required.
            return
        
        if line.startswith(b'# Flotilla'):
            # Occasional case where the first line gets missed off the first
            # time, so reset.
            self._lines = []
            
        self._lines.append(line)
        
        if len(self._lines) == 5 and not self._connected:
            # We have issued our first b'v'
            ready = [False, False, False, False, False,]
            starts = [b'# Flotilla', b'# Version', b'# Serial', b'# User', b'# Dock',]
            for i in range(5):
                ready[i] = self._lines[i].startswith(starts[i])
            if all(ready):
                self._connected = True
                self._lines = []
                self.flotillaCommand(b'd')
        
        if len(self._lines) == 11 and not self._ready:
            # We're connected, and have issued a b'd'
            ready = [False,] * 11
            starts = [b'# SRAM', b'# Loop', b'# Channels', b'# - 0', b'# - 1',
                      b'# - 2', b'# - 3', b'# - 4', b'# - 5', b'# - 6', b'# - 7',]
            for i in range(11):
                ready[i] = self._lines[i].startswith(starts[i])
            if all(ready):
                self._ready = True
                self._lines = []
                self.project.connectModules()
                self.flotillaCommand(b'e')

    def handle_C(self, channel, module):
        print("Found a {} on channel {}".format(module, channel))
        new_module = self.MODULES[module](self, channel)
        self.modules[channel] = new_module
        self.project.connect()
            
    def handle_D(self, channel, module):
        self.modules[channel] = None
        # TODO we should send a message to the project that a new module
        # has been deleted
        
    def handle_U(self, channel, module, data):
        if self.modules[channel] is None:
            # It's possible to get input from a hardware module before
            # everything is connected up. Ignore it until we're ready
            # Rather than using ``self._ready`` we check for ``None`` to avoid
            # any unhandled exceptions.
            return
        j = self.modules[channel].change(data)
        
    def message(self, data):
        self.project.message(data)
        
    def connectedModules(self, type_=None):
        if type_ is None:
            return self.modules.values()
        return [ m for m in self.modules.values() if m is not None and m.module == type_ ]
    
    def firstOf(self, type_):
        modules = self.connectedModules(type_)
        if len(modules) == 0:
            return None
        l = [ (m.channel, m) for m in modules ]
        l.sort()
        return l[0][1]
        
    def lineReceived(self, line):
        parts = line.split(b" ")
        cmd = parts[0]
        if cmd == b'#':
            self.handle_hash(line)
            return
        try:
            channel, module = parts[1].decode('ascii').split('/')
        except IndexError as e:
            # Sometimes, if the Flotilla is particularly overloaded, we get
            # malformed lines. Ignore them.
            print(line)
            return
        channel = int(channel)
        if cmd == b'c':
            self.handle_C(channel, module)
            return
        if cmd == b'd':
            self.handle_D(channel, module)
            return
        if cmd == b'u':
            data = parts[2]
            self.handle_U(channel, module, data)
            return

