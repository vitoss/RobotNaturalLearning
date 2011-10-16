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
        newPosition = self.interpretLine(line)
        if( newPosition != -1 ):
            sequence.appendPosition(newPosition)
        
    
    def interpretLine( self, line ):
        line = line.strip()
    
        #if comments -> continue
        if len(line) == 0 or line[0] == '#':
            return -1
            
        newPosition = -1
        
        splitedLine = line.split('(')
        functionName = splitedLine[0]
        
        #checking if we've got input arguments at all
        if len(splitedLine) > 1:
            inputsString = splitedLine[1].replace(")","")
        
        if functionName == "move":
            #simple for now, list of joints
            joints = self.getJoints(inputsString)
            newPosition = JointPosition(joints[0:self.axisAmount])

        elif functionName == "moveCartesian":
            joints = self.getJoints(inputsString)
            newPosition = CartesianPosition(joints[0:self.axisAmount])

        elif functionName == "moveBy":
            joints = self.getJoints(inputsString)
            newPosition = DeltaJointPosition(joints[0:self.axisAmount])

        elif functionName == "moveCartesianBy":
            joints = self.getJoints(inputsString)
            newPosition = DeltaCartesianPosition(joints[0:self.axisAmount])
        
        return newPosition
        
        
    def getJoints( self, inputsString ):
        return map(float,inputsString.replace(" ","").split(","))