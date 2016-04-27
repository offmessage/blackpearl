from twisted.internet import defer
from twisted.internet import reactor

from .base import FlotillaOutput

import blackpearl.wingdbstub

class MatrixOutput(FlotillaOutput):
    """
    Matrix
    There is much to do. Particularly look at .frames()
    
    """
    module = "matrix"
    
    brightness = 40
    pixels = [0, 0, 0, 0, 0, 0, 0, 0]
    scrollspeed = 0.1
    status = 'STOPPED'
    active = None
    queue = []
    workingframe = []
    lastindex = 0
    loop = False
    
    def reset(self):
        self.queue = []
        self.brightness = 40
        self.status = 'STOPPED'
        self.scrollspeed = 0.1
        self.workingframe = []
        self.lastindex = 0
        self.loop = False
        self.steps = 1
        self.update([0, 0, 0, 0, 0, 0, 0, 0])
    
    def addText(self, text):
        for ch in text:
            i = ord(ch)
            self.queue.extend(ascii_letters[i])
            
    def addColumn(self, column):
        """Bottom is 1, top is 128, we expect it bottom to top"""
        if isinstance(column, int):
            if 0 <= column <= 255:
                self.queue.append(column)
                return
            raise TypeError("column must be an integer between 0 and 255")
        if isinstance(column, list):
            if len(column) == 8:
                if set(column) in [{0},{1},{0,1}]:
                    val = 0
                    for j in range(8):
                        val = val + (2**j)*column[j]
                    self.queue.append(val)
                    return
            raise TypeError("column must be a list of len 8, consisting of {0,1}")
    
    def addFrame(self, frame):
        """left to right"""
        self.queue.extend(frame)
        
    def update(self, pixels):
        self.pixels = pixels
        data = pixels + [self.brightness,]
        self.send(data)
        
    def next_frame(self):
        # XXX Consume the next frame from the queue
        pass
    
    def frames(self):
        self.scroller(steps=8)
        
    def scroll(self):
        self.scroller(steps=1)
        
    @defer.deferredGenerator
    def scroller(self, steps=1):
        self.steps = steps
        self.status = "RUNNING"
        finalindex = len(self.queue) - 7
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
                reactor.callLater(self.scrollspeed, d.callback, self.update(chars))
                wfd = defer.waitForDeferred(d)
                yield wfd
                if self.status == 'RUNNING':
                    self.emit({'scroller': 'step'})
            if not self.loop:
                break
            if self.status == "RUNNING":
                self.lastindex = 0
                self.emit({'scroller': 'loop'})
        if self.status == 'STOPPED':
            self.emit({'scroller': 'finished'})
            
    def pause(self):
        if self.status == "RUNNING":
            self.status = "PAUSED"
        elif self.status == "PAUSED":
            self.status = "RUNNING"
            self.scroller(self.steps)
        self.emit({'scroller': self.status.lower()})
            
            
ascii_letters = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 96, 250, 250, 96, 0, 0],
    [0, 192, 192, 0, 192, 192, 0, 0],
    [40, 254, 254, 40, 254, 254, 40, 0],
    [36, 116, 214, 214, 92, 72, 0, 0],
    [98, 102, 12, 24, 48, 102, 70, 0],
    [12, 94, 242, 186, 236, 94, 18, 0],
    [32, 224, 192, 0, 0, 0, 0, 0],
    [0, 56, 124, 198, 130, 0, 0, 0],
    [0, 130, 198, 124, 56, 0, 0, 0],
    [16, 84, 124, 56, 56, 124, 84, 16],
    [16, 16, 124, 124, 16, 16, 0, 0],
    [0, 1, 7, 6, 0, 0, 0, 0],
    [16, 16, 16, 16, 16, 16, 0, 0],
    [0, 0, 6, 6, 0, 0, 0, 0],
    [6, 12, 24, 48, 96, 192, 128, 0],
    [124, 254, 142, 154, 178, 254, 124, 0],
    [2, 66, 254, 254, 2, 2, 0, 0],
    [70, 206, 154, 146, 246, 102, 0, 0],
    [68, 198, 146, 146, 254, 108, 0, 0],
    [24, 56, 104, 202, 254, 254, 10, 0],
    [228, 230, 162, 162, 190, 156, 0, 0],
    [60, 126, 210, 146, 158, 12, 0, 0],
    [192, 192, 142, 158, 240, 224, 0, 0],
    [108, 254, 146, 146, 254, 108, 0, 0],
    [96, 242, 146, 150, 252, 120, 0, 0],
    [0, 0, 102, 102, 0, 0, 0, 0],
    [0, 1, 103, 102, 0, 0, 0, 0],
    [16, 56, 108, 198, 130, 0, 0, 0],
    [36, 36, 36, 36, 36, 36, 0, 0],
    [0, 130, 198, 108, 56, 16, 0, 0],
    [64, 192, 138, 154, 240, 96, 0, 0],
    [124, 254, 130, 186, 186, 248, 120, 0],
    [62, 126, 200, 200, 126, 62, 0, 0],
    [130, 254, 254, 146, 146, 254, 108, 0],
    [56, 124, 198, 130, 130, 198, 68, 0],
    [130, 254, 254, 130, 198, 124, 56, 0],
    [130, 254, 254, 146, 186, 130, 198, 0],
    [130, 254, 254, 146, 184, 128, 192, 0],
    [56, 124, 198, 130, 138, 206, 78, 0],
    [254, 254, 16, 16, 254, 254, 0, 0],
    [0, 130, 254, 254, 130, 0, 0, 0],
    [12, 14, 2, 130, 254, 252, 128, 0],
    [130, 254, 254, 16, 56, 238, 198, 0],
    [130, 254, 254, 130, 2, 6, 14, 0],
    [254, 254, 112, 56, 112, 254, 254, 0],
    [254, 254, 96, 48, 24, 254, 254, 0],
    [56, 124, 198, 130, 198, 124, 56, 0],
    [130, 254, 254, 146, 144, 240, 96, 0],
    [120, 252, 132, 142, 254, 122, 0, 0],
    [130, 254, 254, 144, 152, 254, 102, 0],
    [100, 246, 178, 154, 206, 76, 0, 0],
    [192, 130, 254, 254, 130, 192, 0, 0],
    [254, 254, 2, 2, 254, 254, 0, 0],
    [248, 252, 6, 6, 252, 248, 0, 0],
    [254, 254, 12, 24, 12, 254, 254, 0],
    [194, 230, 60, 24, 60, 230, 194, 0],
    [224, 242, 30, 30, 242, 224, 0, 0],
    [226, 198, 142, 154, 178, 230, 206, 0],
    [0, 254, 254, 130, 130, 0, 0, 0],
    [128, 192, 96, 48, 24, 12, 6, 0],
    [0, 130, 130, 254, 254, 0, 0, 0],
    [16, 48, 96, 192, 96, 48, 16, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 192, 224, 32, 0, 0, 0],
    [4, 46, 42, 42, 60, 30, 2, 0],
    [130, 254, 252, 18, 18, 30, 12, 0],
    [28, 62, 34, 34, 54, 20, 0, 0],
    [12, 30, 18, 146, 252, 254, 2, 0],
    [28, 62, 42, 42, 58, 24, 0, 0],
    [18, 126, 254, 146, 192, 64, 0, 0],
    [25, 61, 37, 37, 31, 62, 32, 0],
    [130, 254, 254, 16, 32, 62, 30, 0],
    [0, 34, 190, 190, 2, 0, 0, 0],
    [6, 7, 1, 1, 191, 190, 0, 0],
    [130, 254, 254, 8, 28, 54, 34, 0],
    [0, 130, 254, 254, 2, 0, 0, 0],
    [62, 62, 24, 28, 56, 62, 30, 0],
    [62, 62, 32, 32, 62, 30, 0, 0],
    [28, 62, 34, 34, 62, 28, 0, 0],
    [33, 63, 31, 37, 36, 60, 24, 0],
    [24, 60, 36, 37, 31, 63, 33, 0],
    [34, 62, 30, 50, 32, 56, 24, 0],
    [18, 58, 42, 42, 46, 36, 0, 0],
    [0, 32, 124, 254, 34, 36, 0, 0],
    [60, 62, 2, 2, 60, 62, 2, 0],
    [56, 60, 6, 6, 60, 56, 0, 0],
    [60, 62, 14, 28, 14, 62, 60, 0],
    [34, 54, 28, 8, 28, 54, 34, 0],
    [57, 61, 5, 5, 63, 62, 0, 0],
    [50, 38, 46, 58, 50, 38, 0, 0],
    [16, 16, 124, 238, 130, 130, 0, 0],
    [0, 0, 0, 238, 238, 0, 0, 0],
    [130, 130, 238, 124, 16, 16, 0, 0],
    [64, 192, 128, 192, 64, 192, 128, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
