#Test generic delegate
#Author: Witold Wasilewski 2011

from RoboticFramework.RobotController.Delegate.Delegate import Delegate
from RoboticFramework.RobotController.Event.Event import Event

class TestDelegate:
    
    def setup_method(self, method):
        self.delegate = Delegate()
    
    def test_classifyGoodEvent(self):
        event = Event("Sample", 0)
        self.delegate.allowedEventTypes = ["Sample"]
        assert self.delegate.doesHandleEvent(event)
        
    def test_classifyBadEvent(self):
        event = Event("Sample", 0)
        self.delegate.allowedEventTypes = ["Core"]
        assert not self.delegate.doesHandleEvent(event)
    
    def teardown_method(self, method):
        del self.delegate