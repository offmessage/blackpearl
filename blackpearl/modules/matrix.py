from .base import HardwareOutput


class Matrix(HardwareOutput):
    
    module_name = 'matrix'
    
    def reset(self):
        return self.hardware.reset()
    
    def addText(self, text):
        return self.hardware.addText(text)
            
    def addColumn(self, column):
        """Bottom is 1, top is 128, we expect it bottom to top"""
        return self.hardware.addColumn(column)
        
    def addFrame(self, frame):
        """left to right"""
        return self.hardware.addFrame(frame)
        
    def next_frame(self):
        return self.hardware.next_frame()
        
    def frames(self):
        return self.scroller(steps=8)
        
    def scroll(self):
        return self.scroller(steps=1)
        
    def scroller(self, steps=1):
        return self.hardware.scroller(steps)
    
    def pause(self):
        return self.hardware.pause()
    
    
