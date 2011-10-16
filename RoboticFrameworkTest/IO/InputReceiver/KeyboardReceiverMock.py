#Author Witold Wasilewski

from RoboticFramework.IO.InputReceiver.KeyboardReceiver import KeyboardReceiver

class KeyboardReceiverMock (KeyboardReceiver) :
    
    def setPressedKey(self, key):
        self.pressedKey = key;
    
    def getPressedKey(self): 
        if self.pressedKey :
            return pressedKey;
        return 0;