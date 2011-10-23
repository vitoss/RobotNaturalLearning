#Test for position command line interpreter
#Author: Witold Wasilewski 2011

from RoboticFramework.IO.PositionCommandLineInterpreter import PositionCommandLineInterpreter
from RoboticFramework.Command.MoveToPositionCommand import MoveToPositionCommand
from RoboticFramework.Command.CommandList import CommandList
import struct

class TestPositionCommandLineIntepreter:
    
    def setup_method(self, method):
        self.interpreter = PositionCommandLineInterpreter()
    
    def test_simpleJoint(self):
        command = self.interpreter.interpret( "move(60.0,-30.0,30.0,-20.0,10.0,-40.0)")

        assert command.__class__ == MoveToPositionCommand
        assert command.position.getValue()[0] == 60.0
        assert command.position.type == "Joint"
        
    def test_simpleJoint_condensed(self):
        packed = struct.pack("!cffffff", chr(1), 60.0, -30.0, 30.0, -20.0, 10.0, -40.0)
        command = self.interpreter.interpret(packed)

        assert command.__class__ == MoveToPositionCommand
        assert command.position.getValue()[0] == 60.0
        assert command.position.type == "Joint" 

    def test_simpleJoint_condensed_withSpeedFactor(self):
        packed = struct.pack("!cfffffff", chr(2), 60.0, -30.0, 30.0, -20.0, 10.0, -40.0, 0.5)
        command = self.interpreter.interpret(packed)

        assert command.__class__ == MoveToPositionCommand
        assert command.position.getValue()[0] == 60.0
        assert command.position.type == "Joint"
        assert command.speedFactor == 0.5

    def test_comments(self):
        command = self.interpreter.interpret( "#testing line")

        assert command == -1

    def test_newline(self):
        command = self.interpreter.interpret(" \n")

        assert command == -1

    def test_cartesianLine(self):
        command = self.interpreter.interpret("moveCartesian(60.0,-30.0,30.0)")

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "Cartesian"

    def test_deltaJointLine(self):
        command = self.interpreter.interpret("moveBy(60.0,-30.0,30.0,3,3,3)")

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "DeltaJoint"
    
    def test_deltaJointLine_condensed(self):
        packed = struct.pack("!cffffff", chr(3), 60.0, -30.0, 30.0, -20.0, 10.0, -40.0)
        command = self.interpreter.interpret(packed)

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "DeltaJoint"

    def test_deltaJointLine_condensed_withSpeedFactor(self):
        packed = struct.pack("!cfffffff", chr(4), 60.0, -30.0, 30.0, -20.0, 10.0, -40.0, 0.5)
        command = self.interpreter.interpret(packed)

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "DeltaJoint"
        assert command.speedFactor == 0.5

    def test_deltaCartesianLine(self):
        command = self.interpreter.interpret("moveCartesianBy(60.0,-30.0,30.0)")

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "DeltaCartesian"

    def test_axisSimpleJoint(self):
        command = self.interpreter.interpret("moveAxis(1,30.0)")

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "AxisJoint"
        
    def test_axisSimpleJoint_condensed(self):
        packed = struct.pack("!cff", chr(5), 1, 5.0)
        command = self.interpreter.interpret(packed)

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "AxisJoint"

    def test_axisSimpleJoint_condensed_withSpeedFactor(self):
        packed = struct.pack("!cfff", chr(6), 1, 5.0, 0.5)
        command = self.interpreter.interpret(packed)

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "AxisJoint"
        assert command.speedFactor == 0.5

    def test_axisSimpleDeltaJoint(self):
        command = self.interpreter.interpret("moveAxisBy(1,30.0)")

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "AxisDeltaJoint"
        
    def test_axisSimpleDeltaJoint_condensed(self):
        packed = struct.pack("!cff", chr(7), 1, 5.0)
        command = self.interpreter.interpret(packed)

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "AxisDeltaJoint"
    
    def test_axisSimpleDeltaJoint_condensed_withSpeedFactor(self):
        packed = struct.pack("!cfff", chr(8), 1, 5.0, 0.5)
        command = self.interpreter.interpret(packed)

        assert command.__class__ == MoveToPositionCommand
        assert command.position.type == "AxisDeltaJoint"
        assert command.speedFactor == 0.5
        
    def teardown_method(self, method):
        self.interpreter = 0
        self.commandList = 0