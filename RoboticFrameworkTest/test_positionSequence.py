#Testing PositionSequence
#Author: Witold Wasilewski 2011

from RoboticFramework.Position.PositionSequence import PositionSequence
from RoboticFramework.Position.Position import Position

class TestPositionSequence:

	positions = []
	
	def setup_method(self, method):
		self.positions = []
		for i in range(1,7):
			self.positions.append(Position([i]))
			
		self.positionSequence = PositionSequence(self.positions)
	
	def test_append_count(self):
		newPosition = Position([7])
		self.positionSequence.appendPosition(newPosition)
		assert self.positionSequence.amount() == len(self.positions)+1
		
	def test_append_element_at_end(self):
		newPosition = Position([8])
		self.positionSequence.appendPosition(newPosition)
		retrivedPosition = self.positionSequence.getPosition(6)
		
		assert newPosition.getValue() == retrivedPosition.getValue()
	
	def test_current(self):
		retrivedPosition = self.positionSequence.getCurrentPosition()
		
		assert self.positions[0].getValue() == retrivedPosition.getValue()
		
	def test_moveNext(self):
		self.positionSequence.setNextPosition()
		retrivedPosition = self.positionSequence.getCurrentPosition()
		
		assert self.positions[1].getValue() == retrivedPosition.getValue()
		
	def test_isOver(self):
		for j in range(0, len(self.positions)):
			self.positionSequence.setNextPosition()
		
		assert self.positionSequence.isOver() == True
		
	def teardown_method(self, method):
		del self.positions
		del self.positionSequence
		self.positions = []
		self.positionSequence = 0