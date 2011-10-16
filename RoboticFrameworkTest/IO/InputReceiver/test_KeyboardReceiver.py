#Test for keyboard receiver
#Author: Witold Wasilewski 2011

from KeyboardReceiverMock import KeyboardReceiverMock
import Queue

class TestKeyboardReceiver:
    
    def setup_method(self, method):
        queue = Queue.Queue(maxsize=0)
        self.keyboardReceiver = KeyboardReceiverMock("KeyboardReceiverMock", queue)
    
    def testTestLeftArrow(self):
        pass
        
    def teardown_method(self, method):
        self.keyboardRecever = 0
