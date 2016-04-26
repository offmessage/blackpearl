from .base import HardwareOutput


class Matrix(HardwareOutput):
    
    module_name = 'matrix'
    
    def reset(self):
        return self.module.reset()
    
    def addText(self, text):
        return self.module.addText(text)
            
    def addColumn(self, column):
        """Bottom is 1, top is 128, we expect it bottom to top"""
        return self.module.addColumn(column)
        
    def addFrame(self, frame):
        """left to right"""
        return self.module.addFrame(frame)
        
    def next_frame(self):
        return self.module.next_frame()
        
    def frames(self):
        return self.scroller(steps=8)
        
    def scroll(self):
        return self.scroller(steps=1)
        
    def scroller(self, steps=1):
        return self.module.scroller(steps)
    
    def pause(self):
        return self.module.pause()
    
    
