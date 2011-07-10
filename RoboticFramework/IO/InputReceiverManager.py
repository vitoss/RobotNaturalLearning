# Input manager takes care of managing series of input receivers
# Author: Witold Wasilewski 2011

from InputReceiver.InputReceiver import InputReceiver

class InputReceiverManager:
    def __init__(self):
        self.inputReceivers = []
    
    def add(self, receiver):
        self.inputReceivers.append( receiver )
        
    def remove(self, receiver):
        self.inputReceivers.remove( receiver)
        
    def start(self):
        for receiver in self.inputReceivers:
            if receiver.isStarted == 0:
                receiver.startReceiving()
        
    def stop(self):
        for receiver in self.inputReceivers:
            if receiver.isStarted == 1:
                receiver.stopReceiving()
    
    def __del__(self):
        print "Destructor"
        for receiver in self.inputReceivers:
            receiver.stop()