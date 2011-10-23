#Delegate responsible for recording moves
#Author: Witold Wasilewski 2011

from RoboticFramework.RobotController.Delegate.Delegate import Delegate
from RoboticFramework.Position.PositionSequence import PositionSequence
from RoboticFramework.IO.SequenceFileManager import SequenceFileManager

class RobotControllerRecordingDelegate(Delegate):
    
    def __init__(self):
        Delegate.__init__(self)
        self.allowedEventTypes = ["NewPosition", "EndRecordSession", "NewRecordSession", "StartRecord", "StopRecord"]
        self.sequence = PositionSequence()
        self.manager = SequenceFileManager()
        self.recording = False
        
    def notify(self, event):
        if not self.doesHandleEvent(event):
            return
        
        if( event.type == "NewRecordSession" ):
            print "RobotControllerRecordingDelegate: new session named: " + event.data
            self.sessionName = event.data
        elif( event.type == "EndRecordSession" ):
            #saving data
            print "RobotControllerRecordingDelegate: saving file" + self.sessionName
            self.manager.save( self.sequence, self.sessionName )
            self.sessionName = 0 
        elif( event.type == "StartRecord"):
            print "RobotControllerRecordingDelegate: start recording"
            self.recording = True
        elif( event.type == "StopRecord" ):
            self.recording = False
        elif( event.type == "NewPosition" and self.recording ):
            print "RobotControllerRecordingDelegate: add position"
            self.sequence.appendPosition(event.data)
        