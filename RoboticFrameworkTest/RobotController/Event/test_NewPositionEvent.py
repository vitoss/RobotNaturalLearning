#Testing new position event
#Author: Witold Wasilewski

from RoboticFramework.RobotController.Event.NewPositionEvent import NewPositionEvent
import pytest

class TestNewPositionEvent:
    def setup_method(self, method):
        pass
        
    def test_construction_simple(self):
        event = NewPositionEvent("positiondata")
        assert event.data == "positiondata"
    
    def teardown_method(self, method):
        pass