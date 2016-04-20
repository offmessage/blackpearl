from .base import FlotillaOutput

try:
    import blackpearl.wingdbstub
except ImportError:
    pass

class NumberOutput(FlotillaOutput):
    """
    Number
    """
    module = "number"
    
    brightness = 40
    digits = [0, 0, 0, 0, ]
    colon = 0
    apostrophe = 0
    #scrollspeed = 0.1
    #status = 'STOPPED'
    #active = None
    #queue = []
    #workingframe = []
    #lastindex = 0
    #loop = False
    
    def reset(self):
        #self.queue = []
        self.brightness = 40
        #self.status = 'STOPPED'
        #self.active = None
        #self.scrollspeed = 0.1
        #self.workingframe = []
        #self.lastindex = 0
        #self.loop = False
        self.update([0, 0, 0, 0, ])
    
    def set_digit(self, posn, value):
        if not (0 <= value <= 255):
            raise ValueError("value should be between 0 and 255")
        if not (0 <= value <= 3):
            raise ValueError("posn should be between 0 and 3")
        self.digits[posn] = value
        
    def set_number(self, number, pad=None):
        if not (-999 <= number <= 9999):
            raise ValueError("Number is too large. Must be between -999 and 9999")
        digits = list(str(number))
        
        # Need to calculate if we need to pad
        count = len(digits)
        if "." in digits:
            # decimals don't consume a whole digit on the ouput
            count = count - 1
        for i in range(4 - count):
            digits.insert(0, pad)
        
        workingdigit = 0
        for i in range(len(digits)):
            # test if there is a decimal point at [i+1]
            # decide what to set
            # increment workingdigit by 1
            pass
            
                
    def set_time(self, hours, minutes, pad=None):
        if not (0 <= hours <= 23):
            raise ValueError("Hours must be between 0 and 23")
        if not (0 <= minutes <= 59):
            raise ValueError("Minutes must be between 0 and 59")
        self.set_colon(True)
        return
            
    def update(self, digits):
        self.digits = digits
        data = digits + [self.colon, self.apostrophe, self.brightness,]
        self.send(data)
        
    def text(self, text, loop):
        if self.status == 'SCROLLING' or self.status == 'LOOPING':
            return
        if loop:
            self.status = 'LOOPING'
        else:
            self.status = 'SCROLLING'
        pixels = []
        for ch in text:
            i = ord(ch)
            pixels.extend(ascii_letters[i])
        if not loop:
            pixels.extend(ascii_letters[0])
        self.queue = pixels
        if loop:
            self.loopscroll()
        else:
            self.scroll()
        
    @defer.deferredGenerator
    def scroller(self, steps=1):
        self.status = "RUNNING"
        self.active = self.scroller
        finalindex = len(self.queue) - 7
        loopcount = 0
        while self.status == "RUNNING":
            for i in range(self.lastindex, len(self.queue), steps):
                if self.status != "RUNNING":
                    # we are paused or stopped
                    break
                self.lastindex = i
                chars = self.queue[i:i+8]
                if i == finalindex and not self.loop:
                    self.status = "STOPPED"
                    break
                if len(chars) < 8 and self.loop:
                    chars += self.queue[:8-len(chars)]
                d = defer.Deferred()
                if loopcount == 0:
                    # Don't wait to send the first one...
                    # XXX For some reason this doesn't update the matrix?
                    # XXX And doing it as a deferred didn't either...
                    self.update(chars)
                    loopcount += 1
                    continue
                else:
                    reactor.callLater(self.scrollspeed, d.callback, self.update(chars))
                wfd = defer.waitForDeferred(d)
                loopcount += 1
                yield wfd
            if not self.loop:
                break
            if self.status == "RUNNING":
                self.lastindex = 0
            
            
    @defer.deferredGenerator
    def scroll(self, fresh=True):
        pixels = self.queue[:]
        finalindex = len(pixels) - 7
        if fresh:
            # restart the queue from column 1
            self.lastindex = 0
        for i in range(self.lastindex, finalindex):
            if self.status != 'SCROLLING':
                # we are paused (or stopped)
                break
            self.lastindex = i
            chars = pixels[i:i+8]
            if i == finalindex:
                # we've consumed the queue, delete it and set status to stopped
                self.queue = []
                self.status = 'STOPPED'
            d = defer.Deferred()
            reactor.callLater(self.scrollspeed, d.callback, self.update(chars))
            wfd = defer.waitForDeferred(d)
            yield wfd
        
    @defer.deferredGenerator
    def loopscroll(self, fresh=True):
        finalindex = len(self.queue) - 7
        if fresh:
            # restart the queue from column 1
            self.lastindex = 0
        while self.status == 'LOOPING':
            for i in range(self.lastindex, len(self.queue)):
                if self.status != 'LOOPING':
                    break
                self.lastindex = i
                if i <= finalindex:
                    chars = self.queue[i:i+8]
                else:
                    start = i - finalindex
                    chars = self.queue[i:] + self.queue[:start]
                d = defer.Deferred()
                reactor.callLater(self.scrollspeed, d.callback, self.update(chars))
                wfd = defer.waitForDeferred(d)
                yield wfd
            if self.status == 'LOOPING':
                self.lastindex = 0
                    
    @defer.deferredGenerator
    def frames(self, fresh=True):
        self.status = 'SCROLLING'
        self.scrollspeed = 0.3
        pixels = []
        for ch in "1234567890":
            i = ord(ch)
            pixels.extend(ascii_letters[i])
        pixels.extend(ascii_letters[0])
        self.queue = pixels
        #above here is shite
        pixels = self.queue[:]
        finalindex = len(pixels) - 7
        if fresh:
            # restart the queue from column 1
            self.lastindex = 0
        for i in range(self.lastindex, finalindex, 8):
            if self.status != 'SCROLLING':
                # we are paused (or stopped)
                break
            self.lastindex = i
            chars = pixels[i:i+8]
            if i == finalindex:
                # we've consumed the queue, delete it and set status to stopped
                self.queue = []
                self.status = 'STOPPED'
            d = defer.Deferred()
            reactor.callLater(self.scrollspeed, d.callback, self.update(chars))
            wfd = defer.waitForDeferred(d)
            yield wfd
        
    def stop(self):
        if self.status == 'SCROLLING' or self.status == 'LOOPING':
            self.reset()
            
    def pause(self):
        if self.status == "RUNNING":
            self.status = "PAUSED"
            return
        if self.status == "PAUSED":
            self.status = "RUNNING"
            self.active()
        
            
NUM_DOT = 1
NUM_MID = 2
NUM_TL = 4
NUM_BL = 8
NUM_B = 16
NUM_BR = 32
NUM_TR = 64
NUM_T = 128

NUMBERS = [
    NUM_TL + NUM_BL + NUM_T + NUM_B + NUM_TR + NUM_BR,            # 0
    NUM_TR + NUM_BR,                                              # 1
    NUM_BL + NUM_T + NUM_B + NUM_TR + NUM_MID,                    # 2
    NUM_T + NUM_B + NUM_TR + NUM_BR + NUM_MID,                    # 3
    NUM_TR + NUM_TL + NUM_MID + NUM_BR,                           # 4
    NUM_TL + NUM_BR + NUM_MID + NUM_T + NUM_B,                    # 5
    NUM_T + NUM_MID + NUM_B + NUM_BL + NUM_BR + NUM_TL,           # 6
    NUM_T + NUM_TR + NUM_BR,                                      # 7
    NUM_TL + NUM_BL + NUM_T + NUM_B + NUM_TR + NUM_BR + NUM_MID,  # 8
    NUM_TL + NUM_T + NUM_TR + NUM_BR + NUM_MID                    # 9
    ]