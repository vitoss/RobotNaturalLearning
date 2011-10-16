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


class PositionCommandLineInterpreter (PositionLineInterpreter.PositionLineInterpreter):
    
    def __init__(self):
        self.axisAmount = 6
        self.concurentCommands = False
    
    def interpret( self, sequence, line ):
        #all the magic here
        newPositionCommand = self.interpretLine(line)
        sequence.appendPosition(newPositionCommand)
        
    
    def interpretLine( self, line ):
        line = line.strip()
    
        #if comments -> continue
        if line[0] == '#':
            return -1
            
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
        
        newPositionCommand.position = newPosition
        
        return newPositionCommand