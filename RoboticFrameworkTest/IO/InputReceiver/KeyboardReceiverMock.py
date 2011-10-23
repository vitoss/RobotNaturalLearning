#Author Witold Wasilewski

from RoboticFramework.IO.InputReceiver.KeyboardReceiver import KeyboardReceiver

class KeyboardReceiverMock (KeyboardReceiver):
    
    def __init__(self, threadID, name, _queue):
        KeyboardReceiver(threadID, name, _queue)
        self.isStarted = False
    
    def start(self):
        self.isStarted = True
    
    def stop(self):
        self.isStarted = False
    
    def setPressedKey(self, key):
        self.pressedKey = key;
    
    def getPressedKey(self): 
        if self.pressedKey :
            return pressedKey;
        return 0;