#Class for robot controller, which stands for whole integrity
#It provides api for robot sequencer or other class which take command over robot
#Author: Witold Wasilewski 2011

from Event.NewRecordSessionEvent import NewRecordSessionEvent
from Event.NewPositionEvent import NewPositionEvent
from Event.EndRecordSessionEvent import EndRecordSessionEvent
from Event.StopRecordEvent import StopRecordEvent
from Event.StartRecordEvent import StartRecordEvent
from RoboticFramework.Position.JointPosition import JointPosition

class RobotController:
    
    def __init__(self, robotArm, robotModelBounder, Redraw):
        self._robotArm = robotArm
        self._robotModelBounder = robotModelBounder
        self.currentPosition = list(robotArm.JointPositions) #we copy, because we don't want to interfere with robotArm
        self._Redraw = Redraw
        self.isRecording = False
        self.delegates = []
        self.isSessionRecordingActive = False
        self.isRecordingActive = False
        
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
        
    def startRecording(self):
        self.isRecording = True
    
    def stopRecording(self):
        self.isRecording = False
        
    def startProcessingInputQueue(self, queue):
        
        command = 0
        while True:
            #print "Next step"
            if queue.empty() == False :
                if command == 0 or command.isExecuted():
                    print "Start command"
                    
                    if( self.isRecording ):
                        #sending event about new position
                        event = NewPositionEvent(JointPosition(self._robotArm.JointPositions))
                        self.invokeEvent(event)
                        
                    #pop first command and go!
                    command = queue.get()
                    command.execute(self)
                elif command.isAbortable(): 
                    command.stop()
        
    #delegates    
    def addDelegate(self, delegate):
        self.delegates.append(delegate)
    
    def removeDelegate(self, delegate):
        self.delegates.remove(delegate)
    
    def hasDelegate(self, delegate):
        return delegate in self.delegates
        
    def invokeEvent(self, event):
        for delegate in self.delegates:
            delegate.notify(event)
            
    #session recording
    def startRecordSession(self):
        self.isSessionRecordingActive = True
        event = NewRecordSessionEvent("Samples.txt")
        self.invokeEvent(event)
    
    def stopRecordSession(self):
        self.isSessionRecordingActive = False
        
        event = EndRecordSessionEvent()
        self.invokeEvent(event)
        
    def startRecording(self):
        self.isRecording = True
        event = StartRecordEvent()
        self.invokeEvent(event)

    def stopRecording(self):
        self.isRecording = False
        event = StopRecordEvent()
        self.invokeEvent(event)
        
import threading
import time
class CommandWatchdog(threading.Thread):
    
    def run(self):
        command = 0
        while True:
            #print "Next step"
            if self.queue.empty() == False :
                if command == 0 or command.isExecuted():
                    print "Start command"
                    
                    if( self.robotController.isRecording ):
                        #sending event about new position
                        event = NewPositionEvent(JointPosition(self.robotController._robotArm.JointPositions))
                        self.robotController.invokeEvent(event)
                        
                    #pop first command and go!
                    command = self.queue.get()
                    command.execute(self.robotController)
                elif command.isAbortable(): 
                    command.stop()

            time.sleep(0.1)
                
        