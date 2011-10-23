#Event base type
#Author: Witold Wasilewski 2011

class Event:
    
    def __init__(self, _type, data):
        self.data = data
        self.type = _type