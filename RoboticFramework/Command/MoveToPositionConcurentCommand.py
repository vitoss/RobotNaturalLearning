#Command executing move to certain position
#Author: Witold Wasilewski 2011

import ConcurentCommand
import threading 

class MoveToPositionConcurentCommand(ConcurentCommand.ConcurentCommand):
    
    def __init__(self):
        ConcurentCommand.ConcurentCommand.__init__(self)
        self.position = -1
        self.speedFactor = 1
    
    def execute(self, robotController):
        self.robotController = robotController
        self.start()
        
        return True
    
    def run(self):
        #checking speed factor just in case
        if self.speedFactor < 0:
            self.speedFactor = 0
        elif self.speedFactor > 1:
            self.speedFactor = 1
    
        if self.position != -1:
            self.robotController.moveTo(self.position, self.speedFactor)
    
    def stop(self):
        self.robotController.stopMove()
    
    def isExecuted(self):
        return self.robotController.isIdle()
        
    def isAbortable(self):
        return True
        