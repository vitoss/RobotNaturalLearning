#Robot controller stug to mimic robot controller
#Author: Witold Wasilewski 2011

class RobotController:

	def __init__(self):
		self._currentPosition = 0
		self._stepCount = 0
		
	def moveTo(self, position):
		self._currentPosition = position
		self._stepCount += 1
	
	def getCurrentPosition(self):
		return self._currentPosition;
		
	def getStepCount(self):
		return self._stepCount