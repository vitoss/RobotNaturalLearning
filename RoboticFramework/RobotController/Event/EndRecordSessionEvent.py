#Event known as end record session
#Author: Witold Wasilewski

from Event import Event

class EndRecordSessionEvent(Event):
    
    def __init__(self):
        self.data = 0
        self.type = "EndRecordSession"
