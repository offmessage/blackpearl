
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
        

        