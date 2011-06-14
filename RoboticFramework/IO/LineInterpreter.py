#Intepreting Single line from sequence file
#Author: Witold Wasilewski 2011

from RoboticFramework.Position.JointPosition import JointPosition

class LineInterpreter:
	
	def interpret( self, sequence, line ):
		#all the magic here
		
		#simple for now, list of joints
		joints = map(float,line.replace(" ","").split(","))
		newPosition = JointPosition(joints)
		sequence.appendPosition(newPosition)