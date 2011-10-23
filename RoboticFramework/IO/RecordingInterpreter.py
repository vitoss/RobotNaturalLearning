#Recording Interpreter
#Author: Witold Wasilewski 2011

from RoboticFramework.Command.BeginRecordSessionCommand import BeginRecordSessionCommand
from RoboticFramework.Command.EndRecordSessionCommand import EndRecordSessionCommand
from RoboticFramework.Command.StartRecordCommand import StartRecordCommand
from RoboticFramework.Command.StopRecordCommand import StopRecordCommand
import struct

class RecordingInterpreter:
    
    def interpret(self, line):
        
        line = line.strip()
    
        #if comments -> continue
        if line == "" or line[0] == '#':
            return -1
                        
        if line.find("(") == -1:
            return self.interpretCondensed(line)
        else:
            return self.interpretLine(line)

    def interpretCondensed(self, line):
        #get function name to have format - first byte
        unpackedFormatType = ord(struct.unpack("!c", line[0])[0])
        
        if unpackedFormatType < 20:
            return -1

        formats = ["!c", "!c", "!c", "!c"]
        format = formats[unpackedFormatType-20]
        unpackedLine = struct.unpack(format, line)
    
        if unpackedFormatType == 20:
            return BeginRecordSessionCommand()
        elif unpackedFormatType == 21:
            return EndRecordSessionCommand()
        elif unpackedFormatType == 22:
            return StartRecordCommand()
        elif unpackedFormatType == 23:
            return StopRecordCommand()
        
    def interpretLine(self, line):
        line = line.strip()
        
        functionName = self.getFunctionName(line)

        if( functionName == "BeginRecordSession"):
            sessionName = self.getArgument(line)
            return BeginRecordSessionCommand() #sessionName
        elif( functionName == "EndRecordSession"):
            return EndRecordSessionCommand()
        elif( functionName == "StartRecording"):
            return StartRecordCommand()
        elif( functionName == "StopRecording"):
            return StopRecordCommand()
        
        return -1
    
    def getFunctionName(self, line):
        splittedLine = line.split("(")
        return splittedLine[0]
    
    def getArgument(self, line):
        splittedLine = line.split("(")
        argument = splittedLine[1].replace(")", "")
        return argument
        
        