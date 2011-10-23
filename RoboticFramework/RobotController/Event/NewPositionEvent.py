#Event known as new position
#Author: Witold Wasilewski

from Event import Event

class NewPositionEvent(Event):
    
    def __init__(self, data):
        self.data = data
        self.type = "NewPosition"
        