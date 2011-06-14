#Class responsible for executing in order sequence of positions
#Author: Witold Wasilewski 2011

class SequenceExecutor:
	#_robotController = 0
	#_sequence = 0
	
	def __init__( self, robotController, sequence ):
		self._sequence = sequence
		self._robotController = robotController
		
	def executeOnce( self ):
		while self._sequence.isOver() == False:
			currentPosition = self._sequence.getCurrentPosition()
			self._robotController.moveTo(currentPosition)
			self._sequence.setNextPosition()
	
	def execute( self, amount = 1 ):
		for i in range(0, amount):
			self.executeOnce()
			self._sequence.reset()
	
	def isOver(self):
		return self._sequence.isOver()