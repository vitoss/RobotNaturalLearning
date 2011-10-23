#Generic delegate class
#Author: Witold Wasilewski 2011

class Delegate:
    
    def __init__(self):
        self.allowedEventTypes = []
    
    def doesHandleEvent(self, event):
        return event.type in self.allowedEventTypes
        
    def notify(self, event):
        if not self.doesHandleEvent(event):
            return