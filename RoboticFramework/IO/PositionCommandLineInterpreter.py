#Intepreting Single line from sequence file as command
#Author: Witold Wasilewski 2011

from RoboticFramework.Position.JointPosition import JointPosition
from RoboticFramework.Position.DeltaJointPosition import DeltaJointPosition
from RoboticFramework.Position.CartesianPosition import CartesianPosition
from RoboticFramework.Position.DeltaCartesianPosition import DeltaCartesianPosition
from RoboticFramework.Position.AxisDeltaJointPosition import AxisDeltaJointPosition
from RoboticFramework.Position.AxisJointPosition import AxisJointPosition
import RoboticFramework.Command.MoveToPositionCommand as MoveToPositionCommand
import RoboticFramework.Command.MoveToPositionConcurentCommand as MoveToPositionConcurentCommand
import PositionLineInterpreter
import struct

class PositionCommandLineInterpreter (PositionLineInterpreter.PositionLineInterpreter):
    
    def __init__(self):
        self.axisAmount = 6
        self.concurentCommands = False
    
    def interpretForSequence( self, sequence, line ):
        #all the magic here
        newPositionCommand = self.interpretLine(line)
        sequence.appendPosition(newPositionCommand)
        
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
        
        if unpackedFormatType > 8:
            return -1
        
        formats = ["!cffffff", "!cfffffff", "!cffffff", "!cfffffff", "!cff", "!cfff", "!cff", "!cfff", "!c", "!c", "!c", "!c"]
        format = formats[unpackedFormatType-1]
        unpackedLine = struct.unpack(format, line)
        
        if self.concurentCommands:
            newPositionCommand = MoveToPositionConcurentCommand.MoveToPositionConcurentCommand()
        else:
            newPositionCommand = MoveToPositionCommand.MoveToPositionCommand()
            
        newPosition = -1
        
        if unpackedFormatType == 1:
            newPosition = JointPosition(unpackedLine[1:7])
        elif unpackedFormatType == 2:
            newPosition = JointPosition(unpackedLine[1:7])
            newPositionCommand.speedFactor = unpackedLine[7]
        elif unpackedFormatType == 3:
            newPosition = DeltaJointPosition(unpackedLine[1:7])
        elif unpackedFormatType == 4:
            newPosition = DeltaJointPosition(unpackedLine[1:7])
            newPositionCommand.speedFactor = unpackedLine[7]
        elif unpackedFormatType == 5:
            newPosition = AxisJointPosition(unpackedLine[1:3])
        elif unpackedFormatType == 6:
            newPosition = AxisJointPosition(unpackedLine[1:3])
            newPositionCommand.speedFactor = unpackedLine[3]
        elif unpackedFormatType == 7:
            newPosition = AxisDeltaJointPosition(unpackedLine[1:3])
        elif unpackedFormatType == 8:
            newPosition = AxisDeltaJointPosition(unpackedLine[1:3])
            newPositionCommand.speedFactor = unpackedLine[3]
        else:
            return -1
        
        newPositionCommand.position = newPosition
        
        return newPositionCommand
        
        
    def interpretLine( self, line ):

        newPosition = -1
        splitedLine = line.split('(')
        functionName = splitedLine[0]
        
        if self.concurentCommands:
            newPositionCommand = MoveToPositionConcurentCommand.MoveToPositionConcurentCommand()
        else:
            newPositionCommand = MoveToPositionCommand.MoveToPositionCommand()
        
        #checking if we've got input arguments at all
        if len(splitedLine) > 1:
            inputsString = splitedLine[1].replace(")","")
        
        if functionName == "move":
            #simple for now, list of joints
            joints = self.getFuctionArguments(inputsString)
            newPosition = JointPosition(joints[0:self.axisAmount])
            
            if len(joints) == 7:
                newPositionCommand.speedFactor = joints[6]
                
        elif functionName == "moveCartesian":
            joints = self.getFuctionArguments(inputsString)
            newPosition = CartesianPosition(joints[0:self.axisAmount])
            
            if len(joints) == 7:
                newPositionCommand.speedFactor = joints[6]
            
        elif functionName == "moveBy":
            joints = self.getFuctionArguments(inputsString)
            newPosition = DeltaJointPosition(joints[0:self.axisAmount])
            
            if len(joints) == 7:
                newPositionCommand.speedFactor = joints[6]
                
        elif functionName == "moveCartesianBy":
            joints = self.getFuctionArguments(inputsString)
            newPosition = DeltaCartesianPosition(joints[0:self.axisAmount])
            
            if len(joints) == 7:
                newPositionCommand.speedFactor = joints[6]
                
        elif functionName == "moveAxis":
            joints = self.getFuctionArguments(inputsString)
            newPosition = AxisJointPosition(joints[0:2])
            
            if len(joints) == 3:
                newPositionCommand.speedFactor = joints[2]
        
        elif functionName == "moveAxisBy":
            joints = self.getFuctionArguments(inputsString)
            newPosition = AxisDeltaJointPosition(joints[0:2])
            
            if len(joints) == 3:
                newPositionCommand.speedFactor = joints[2]
        else:
            return -1
        
        newPositionCommand.position = newPosition
        
        return newPositionCommand