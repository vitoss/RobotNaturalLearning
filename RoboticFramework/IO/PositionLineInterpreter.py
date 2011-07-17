#Intepreting Single line from sequence file
#Author: Witold Wasilewski 2011

from RoboticFramework.Position.JointPosition import JointPosition
from RoboticFramework.Position.DeltaJointPosition import DeltaJointPosition
from RoboticFramework.Position.CartesianPosition import CartesianPosition
from RoboticFramework.Position.DeltaCartesianPosition import DeltaCartesianPosition
import RoboticFramework.Command.MoveToPositionCommand as MoveToPositionCommand
import LineInterpreter

class PositionLineInterpreter (LineInterpreter.LineInterpreter):
    
    def __init__(self):
        self.axisAmount = 6
    
    def interpret( self, sequence, line ):
        #all the magic here
        sequence.appendPosition(self.interpretLine(line))
        
    
    def interpretLine( self, line ):
        line = line.strip()
    
        #if comments -> continue
        if line[0] == '#':
            return -1
            
        newPosition = -1
        splitedLine = line.split('(')
        functionName = splitedLine[0]
        
        #checking if we've got input arguments at all
        if len(splitedLine) > 1:
            inputsString = splitedLine[1].replace(")","")
        
        
        newPositionCommand = MoveToPositionCommand.MoveToPositionCommand()
        
        if functionName == "move":
            #simple for now, list of joints
            joints = map(float,inputsString.replace(" ","").split(","))
            newPosition = JointPosition(joints[0:self.axisAmount])
            
            if len(joints) == 7:
                newPositionCommand.speedFactor = joints[6]
                
        elif functionName == "moveCartesian":
            joints = map(float,inputsString.replace(" ","").split(","))
            newPosition = CartesianPosition(joints[0:self.axisAmount])
            
            if len(joints) == 7:
                newPositionCommand.speedFactor = joints[6]
                
        elif functionName == "moveBy":
            joints = map(float,inputsString.replace(" ","").split(","))
            newPosition = DeltaJointPosition(joints[0:self.axisAmount])
            
            if len(joints) == 7:
                newPositionCommand.speedFactor = joints[6]
                
        elif functionName == "moveCartesianBy":
            joints = map(float,inputsString.replace(" ","").split(","))
            newPosition = DeltaCartesianPosition(joints[0:self.axisAmount])
            
            if len(joints) == 7:
                newPositionCommand.speedFactor = joints[6]
        
        newPositionCommand.position = newPosition
        
        return newPositionCommand