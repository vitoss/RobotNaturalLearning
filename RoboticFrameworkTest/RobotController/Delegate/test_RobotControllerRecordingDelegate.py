#Tests for RobotControllerRecordingDelegate
#Author: Witold Wasilewski 2011

from config import Config
from RoboticFramework.RobotController.Delegate.RobotControllerRecordingDelegate import RobotControllerRecordingDelegate
from RoboticFramework.RobotController.Event.NewPositionEvent import NewPositionEvent
from RoboticFramework.RobotController.Event.Event import Event
from RoboticFramework.Position.JointPosition import JointPosition
from RoboticFramework.Position.PositionSequence import PositionSequence

class TestRobotControllerRecordingDelegate:
    def setup_method(self, method):
        self.delegate = RobotControllerRecordingDelegate()
        self.delegate.sequence = PositionSequence()
        
    def test_gotGoodNotify_amount(self):
        self.delegate.recording = True
        position = JointPosition([10,10,10,10,10,10])
        event = NewPositionEvent(position)
        
        self.delegate.notify(event)
        assert self.delegate.sequence.amount() == 1

    def test_gotGoodNotify_lastPosition(self):
        self.delegate.recording = True
        position = JointPosition([10,10,10,10,10,10])
        event = NewPositionEvent(position)

        self.delegate.notify(event)
        assert self.delegate.sequence.getCurrentPosition() == position
    
    
    def test_gotBadNotify(self):
        event = Event(0,"Wrong")
        
        self.delegate.notify(event)
        assert self.delegate.sequence.amount() == 0
    
    def test_sequenceBuilding(self):
        self.delegate.recording = True
        
        position = JointPosition([10,10,10,10,10,10])
        event = NewPositionEvent(position)
        position2 = JointPosition([10,10,10,10,10,10])
        event2 = NewPositionEvent(position2)
        
        self.delegate.notify(event)
        self.delegate.notify(event2)
        
        assert self.delegate.sequence.amount() == 2
        assert self.delegate.sequence.getPosition(1) == position2
        assert self.delegate.sequence.getCurrentPosition() == position
        
    def teardown_method(self, method):
        del self.delegate