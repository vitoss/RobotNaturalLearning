#Event known as start record
#Author: Witold Wasilewski

from Event import Event

class StopRecordEvent(Event):
    
    def __init__(self):
        self.data = 0
        self.type = "StopRecord"
