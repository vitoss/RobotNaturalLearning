#Command base class
#Author: Witold Wasilewski

class Command:
    
    def __init__(self):
        pass
        
    def execute(self, robotController):
        pass
        
    def run(self):
        pass
        
    def stop(self):
        pass
    
    def isExecuted(self):
        return True
        
    def isAbortable(self):
        return False
        