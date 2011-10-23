#Event known as start record
#Author: Witold Wasilewski

from Event import Event

class StartRecordEvent(Event):
    
    def __init__(self):
        self.data = 0
        self.type = "StartRecord"
