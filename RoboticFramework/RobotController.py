#Class for robot controller, which stands for whole integrity
#It provides api for robot sequencer or other class which take command over robot
#Author: Witold Wasilewski 2011

class RobotController:
	
	def __init__(self, robotArm, robotModelBounder, Redraw):
		self._robotArm = robotArm
		self._robotModelBounder = robotModelBounder
		self.currentPosition = list(robotArm.JointPositions) #we copy, because we don't want to interfere with robotArm
		self._Redraw = Redraw
		
	def moveTo(self, position):
		if position.type == "Joint" :
			positionValue = position.getValue()
			
			#setting position
			for i in range(0, self._robotArm.getJointAmount()):
				self._robotArm.rotateTo(i, positionValue[i])
			
			#moving arm to set position
			while self._robotArm.isMovementDone() == False:
				self._robotArm.makeMove()
				self._robotModelBounder.bound()
				self._Redraw() #TODO think about Visualizer???
		else:
			raise Exception( "Not implemeneted type of position" )
		
		#saving position when exception not thrown
		self.currentPosition = position