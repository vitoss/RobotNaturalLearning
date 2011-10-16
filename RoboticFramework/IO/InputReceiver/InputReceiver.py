#Base class for various input receivers
#Author: Witold Wasilewski

import sys
import threading

class InputReceiver(threading.Thread):
    def __init__(self, threadID, name, _queue):
        threading.Thread.__init__(self)
        print "Intializing thread"
        print name
        
        self.threadID = threadID
        self.customName = name
        self.isStarted = 0
        self.queue = _queue
        self.daemon = True
        
		
    def run(self):
		print "Starting " + self.customName
		
		print "Exiting " + self.customName
	
    def startReceiving(self):
        self.isStarted = 1
	
    def stopReceiving(self):
        self.isStarted = 0
		
