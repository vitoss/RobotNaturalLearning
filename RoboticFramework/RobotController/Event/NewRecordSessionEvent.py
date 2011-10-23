#Event known as new record session
#Author: Witold Wasilewski

from Event import Event

class NewRecordSessionEvent(Event):
    
    def __init__(self, data):
        self.data = data
        self.type = "NewRecordSession"
