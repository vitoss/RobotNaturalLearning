#Testing recroding interpreter
#Author: Witold Wasilewski 2011

from RoboticFramework.IO.RecordingInterpreter import RecordingInterpreter
from RoboticFramework.Command.BeginRecordSessionCommand import BeginRecordSessionCommand
from RoboticFramework.Command.EndRecordSessionCommand import EndRecordSessionCommand
from RoboticFramework.Command.StartRecordCommand import StartRecordCommand
from RoboticFramework.Command.StopRecordCommand import StopRecordCommand
import struct

class TestRecordingInterpreter:
    
    def setup_method(self, method):
        self.interpreter = RecordingInterpreter()
        
    def test_interpret_startSessionCommand(self):
        line = "BeginRecordSession(lambada)"
        command = self.interpreter.interpret(line)
        
        assert command.__class__ == BeginRecordSessionCommand
    
    def test_interpret_startSessionCommand_condensed(self):
        packed = struct.pack("!c", chr(20))
        command = self.interpreter.interpret(packed)

        assert command.__class__ == BeginRecordSessionCommand
    
    def test_interpret_stopSessionCommand(self):
        line = "EndRecordSession()"
        command = self.interpreter.interpret(line)
        
        assert command.__class__ == EndRecordSessionCommand
    
    def test_interpret_stopSessionCommand_condensed(self):
        packed = struct.pack("!c", chr(21))
        command = self.interpreter.interpret(packed)

        assert command.__class__ == EndRecordSessionCommand    
        
    def test_interpret_startRecCommand(self):
        line = "StartRecording()"
        command = self.interpreter.interpret(line)
        
        assert command.__class__ == StartRecordCommand
        
    def test_interpret_startRecCommand_condensed(self):
        packed = struct.pack("!c", chr(22))
        command = self.interpreter.interpret(packed)

        assert command.__class__ == StartRecordCommand        
        
    def test_interpret_stopRecCommand(self):
        line = "StopRecording()"
        command = self.interpreter.interpret(line)
        
        assert command.__class__ == StopRecordCommand
        
    def test_interpret_stopRecCommand_condensed(self):
        packed = struct.pack("!c", chr(23))
        command = self.interpreter.interpret(packed)

        assert command.__class__ == StopRecordCommand
        
    def teardown_method(self, method):
        del self.interpreter