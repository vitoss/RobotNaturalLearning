# Robot animation runner, integrates robot's abstract model with 3D model
# Author: Witold Wasilewski 2011

from math import *
import RobotArm

class RobotModelBounder:
	#_RobotArm 
	_Links = []
	#_Tool = 0
	#_ToolPiston = 0
	
	def __init__( self, robotArm, links, tool, toolPiston ):
		self._RobotArm = robotArm
		self._Links = links
		self._Tool = tool
		self._ToolPiston = toolPiston
	
	def bound(self):
		positions = self._RobotArm.JointPositions
		
		self._Links[1].rot = [0, 0, float(radians(positions[0]))]##### rotating link two around its pivot point using euler angles
		self._Links[2].rot =[ 0, float(radians(positions[1])), 0]                
		self._Links[3].rot = [0, float(radians(positions[2])), 0]
		self._Links[4].rot = [float(radians(positions[3])), 0, 0]
		self._Links[5].rot = [0, float(radians(positions[4])), 0]
		self._Tool.rot = [float(radians(positions[5])), 0, 0]
		self._ToolPiston.rot = [0, 0, 0] #there is not rotation here but it is required to update the object
		
		
			