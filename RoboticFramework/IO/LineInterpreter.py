#Intepreting Single line from sequence file
#Author: Witold Wasilewski 2011

from RoboticFramework.Position.JointPosition import JointPosition
from RoboticFramework.Position.DeltaJointPosition import DeltaJointPosition
from RoboticFramework.Position.CartesianPosition import CartesianPosition
from RoboticFramework.Position.DeltaCartesianPosition import DeltaCartesianPosition

class LineInterpreter:
	
	def interpret( self, sequence, line ):
		#all the magic here
		
		#if comments -> continue
		if line[0] == '#':
			return
			
		splitedLine = line.split('(')
		functionName = splitedLine[0]
		
		#checking if we've got input arguments at all
		if len(splitedLine) > 1:
			inputsString = splitedLine[1].replace(")","")
		
		if functionName == "move":
			#simple for now, list of joints
			joints = map(float,inputsString.replace(" ","").split(","))
			newPosition = JointPosition(joints)
			sequence.appendPosition(newPosition)
		elif functionName == "moveCartesian":
			joints = map(float,inputsString.replace(" ","").split(","))
			newPosition = CartesianPosition(joints)
			sequence.appendPosition(newPosition)
		elif functionName == "moveBy":
			joints = map(float,inputsString.replace(" ","").split(","))
			newPosition = DeltaJointPosition(joints)
			sequence.appendPosition(newPosition)
		elif functionName == "moveCartesianBy":
			joints = map(float,inputsString.replace(" ","").split(","))
			newPosition = DeltaCartesianPosition(joints)
			sequence.appendPosition(newPosition)