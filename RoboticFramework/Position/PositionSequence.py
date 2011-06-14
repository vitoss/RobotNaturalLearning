#Class holding many positions, which should be adressed sequentally
#Author: Witold Wasilewski 2011

class PositionSequence:
	_positions = []
	index = -1
	
	def __init__(self, positions = []):
		self._positions = list(positions)
		self.index = 0
		
	def getCurrentPosition( self ):
		return self._positions[self.index]
	
	def setNextPosition( self ):
			self.index += 1
	
	def appendPosition( self, position ):
		self._positions.append(position)
		
	def isOver( self ):
		return self.index >= self.amount()
	
	def reset( self ):
		self.index = 0
		
	def amount(self):
		return len(self._positions)
		
	def getPosition(self, index):
		return self._positions[index];