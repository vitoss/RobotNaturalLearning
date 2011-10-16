#Command base class
#Author: Witold Wasilewski

import threading
from Command import Command

class ConcurentCommand(Command, threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.isSequential = True
        
    def execute(self, robotController):
        pass
        
    def run(self):
        pass
        
    def stop(self):
        pass
    
    def isExecuted(self):
        return True
        
    def isAbortable(self):
        return not self.isSequential
        