#Class responsible for receiving keyboard interrupts
#Author: Witold Wasilewski 2011

import time
from InputReceiver import InputReceiver 
import RoboticFramework.Position.DeltaJointPosition as DeltaJointPosition

class KeyboardReceiver  : #(InputReceiver):
	
    def __init__(self, name, _queue):
        self.customName = name
        self.queue = _queue
        self.isStarted = 1
    
    def start(self):
        self.run()

    def run(self):
        
        print "Starting " + self.customName
        while True: 
            time.sleep(0.05)
            keyPressed = self.getPressedKey()
            print keyPressed
            
            if keyPressed == 113:
                print "BREAK"
                break
        
            if keyPressed == 119 :
                print "New delta"
                self.queue.put(DeltaJointPosition.DeltaJointPosition([5,5,5,5,5,5]))
                
            #nameInput = raw_input("Enter your name:")
            #print "Hello", nameInput
            #raw_input("Press any key to exit.") 
		
        print "Exiting " + self.customName
        
    #Returns key or 0 if not key is pressed
    def getPressedKey(self): 
        
        try:
            #LINUX implementation
            import select
        
            i,o,e = select.select([sys.stdin],[],[],0.0001)
            for s in i:
                if s == sys.stdin:
                    input = sys.stdin.readline()
                    return input
            return 0
        except Exception:
            #WINDOWS implementation
            import msvcrt
            
            x = msvcrt.kbhit()
            if x: 
                ret = ord(msvcrt.getch()) 
            else: 
                ret = 0 
            return ret