#Testing stop recording command
#Author: Witold Wasilewski

from RoboticFramework.Command.EndRecordSessionCommand import EndRecordSessionCommand
from RoboticFramework.Command.BeginRecordSessionCommand import BeginRecordSessionCommand
from DummyRobotController import DummyRobotController

class TestEndRecordSessionCommand:
    
    def setup_method(self, method):
        self.robotController = DummyRobotController()
    
    def test_command_simple(self):
        #test if command stop record session in controller
        command = BeginRecordSessionCommand()
        command.execute(self.robotController)
        
        command2 = EndRecordSessionCommand()
        command2.execute(self.robotController)
        
        assert not self.robotController.isSessionRecordingActive
    
    def teardown_method(self, method):
        pass