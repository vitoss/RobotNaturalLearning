#Test generic event
#Author: Witold Wasilewski

from RoboticFramework.RobotController.Event.Event import Event

class TestEvent:
    def setup_method(self, method):
        pass
    
    def test_constuctor_simple(self):
        event = Event("type", "data")
        assert event.data == "data"
        assert event.type == "type"
                
    def teardown_method(self, method):
        pass