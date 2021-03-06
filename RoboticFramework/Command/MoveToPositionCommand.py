#Command executing move to certain position
#Author: Witold Wasilewski 2011

import Command
import threading 

class MoveToPositionCommand(Command.Command):
    
    def __init__(self):
        Command.Command.__init__(self)
        self.position = -1
        self.speedFactor = 1
    
    def execute(self, robotController):
        self.robotController = robotController
        
        #checking speed factor just in case
        if self.speedFactor < 0:
            self.speedFactor = 0
        elif self.speedFactor > 1:
            self.speedFactor = 1
    
        if self.position != -1:
            self.robotController.moveTo(self.position, self.speedFactor)
        
        return True
        
    def stop(self):
        self.robotController.stopMove()
    
    def isExecuted(self):
        return self.robotController.isIdle()
        