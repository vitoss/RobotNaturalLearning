#Class for robot controller, which stands for whole integrity
#It provides api for robot sequencer or other class which take command over robot
#Author: Witold Wasilewski 2011

class RobotController:
    
    def __init__(self, robotArm, robotModelBounder, Redraw):
        self._robotArm = robotArm
        self._robotModelBounder = robotModelBounder
        self.currentPosition = list(robotArm.JointPositions) #we copy, because we don't want to interfere with robotArm
        self._Redraw = Redraw
        
    #position - target position
    #speedFactor - float 0-1, we multiply physical robotArm speed with this factor
    def moveTo( self, position, speedFactor):
        #setting robot arm speed
        self._robotArm.setSpeedFactor(speedFactor)
        
        if position.type == "Joint" :
            positionValue = position.getValue()
            
            #setting position
            for i in range(0, self._robotArm.getJointAmount()):
                self._robotArm.rotateTo(i, positionValue[i])
            
            self.executeMove()
        elif position.type == "DeltaJoint":
            positionValue = position.getValue()
            
            #setting position
            for i in range(0, self._robotArm.getJointAmount()):
                self._robotArm.rotateBy(i, positionValue[i])
            
            self.executeMove()
        
        elif position.type == "AxisJoint":
            positionValue = position.getValue()
            
            #setting position
            self._robotArm.rotateTo(int(positionValue[0]), positionValue[1])
            
            self.executeMove()
            
        elif position.type == "AxisDeltaJoint":
            positionValue = position.getValue()
            
            #setting position
            self._robotArm.rotateBy(int(positionValue[0]), positionValue[1])
            
            self.executeMove()
            
        else:
            raise Exception( "Not implemented type of position: ", position.type )
        
        #saving position when exception not thrown
        self.currentPosition = position
        
    
    def executeMove(self):
        #moving arm to set position
        while self._robotArm.isMovementDone() == False:
            #print "Execute move effective"
            self._robotArm.makeMove()
            self._robotModelBounder.bound()
            self._Redraw() 
                
        
    def stopMove(self):
        self._robotArm.stopAtCurrentPosition()
    
    def isIdle(self):
        return self._robotArm.isMovementDone()
        
    def startProcessingInputQueue(self, queue):
            command = 0
            while True:
                #print "Next step"
                if queue.empty() == False :
                    if command == 0 or command.isExecuted():
                        print "Start command"
                        #pop first command and go!
                        command = queue.get()
                        command.execute(self)
                    elif command.isAbortable(): 
                        command.stop()
            
    