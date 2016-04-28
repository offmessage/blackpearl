"""
=======================================
Black Pearl: For twisted little pirates
=======================================

modules/base.py

Base class for our modules.
"""

from collections import Counter


class BaseModule:
    
    module_name = None
    listening_for = []
    
    hardware_required = []
    _all_connected = False
    
    def __init__(self, project):
        self.project = project
        self._checkRequirements()
        self.setup()
        
    def setup(self):
        pass
    
    def _checkRequirements(self):
        if not self.hardware_required:
            return

        # Here we create attributes for each piece of hardware.
        # Using the example ['motor', 'motor', 'slider'] we would end up
        # with .motor1, .motor2, and .slider
        
        connected = [ m for m in self.project.flotilla.modules.values() if m is not None ]
        names = [ m.module for m in connected ]

        # Test to see if we have more than one of the same module defined
        # e.g. ['motor', 'motor', 'slider'].
        # Counter() creates a dictionary of the form {'motor': 2, 'slider': 1}
        count = Counter(names)
        simple_case = all([ x == 1 for x in count.values() ])
        if simple_case:
            working_list = list(zip(connected, names))
        else:
            # This is a bit messy, but it's where we construct the names when
            # there is more than one of particular module (e.g. motor1
            # and motor2)
            working_list = []
            namedict = {}
            for k, v in count.items():
                namedict[k] = []
                if v == 1:
                    namedict[k] = [k,]
                    continue
                for i in range(1, v+1):
                    namedict[k].append('{}{}'.format(k, i))
                    
            for m in connected:
                module = m
                attrname = namedict[m.module].pop(0)
                working_list.append((module, attrname))
                
        found = []
        missing = []
        
        # What we need to do is create a Counter out of self.hardware_required
        # and then compare the keys of that counter to the keys of Counter(names)
        # and bail until that is satisfied
        check = Counter(self.hardware_required)
        for k, v in check.items():
            if k not in count:
                return
            if count[k] > v:
                return
            
        for h in self.hardware_required:
            worknames = names.copy()
            if h in worknames:
                index = names.index(h)
                names.remove(h)
                module, attrname = working_list.pop(index)
                setattr(self, attrname, module)
                found.append(h)
            else:
                missing.append(h)
        if len(self.hardware_required) == len(found):
            self.project.log('INFO', 'All requirments met \o/')
            self._all_connected = True
        else:
            self.project.log('ERROR', 'Requirements met: ' + ', '.join(found))
            self.project.log('ERROR', 'Missing modules: ' + ', '.join(missing))

    def dispatch(self, data):
        for l in self.listening_for:
            if l in data:
                self.data(data)
        
    def data(self, data):
        pass

    def emit(self, data):
        if data is None:
            return data
        output = {self.module_name: data}
        self.project.message(output)
        
