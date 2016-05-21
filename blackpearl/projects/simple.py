from .base import BaseProject

class Flotilla():
    
    def add_module(self, klass):
        if not hasattr(self, "project"):
            self.project = BaseProject()
        self.project.add_module(klass)
        
    def run(self):
        self.project.run()
        
flotilla = Flotilla()
