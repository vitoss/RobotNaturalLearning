#Test scenerios for SequenceExecutor
#Author Witold Wasilewski 2011

from RoboticFramework.Position.PositionSequence import PositionSequence
from RoboticFramework.Position.Position import Position
from RoboticFramework.SequenceExecutor import SequenceExecutor
from Stug.RobotController import RobotController

class TestSequenceExecutor:
	
	positions = []
	
	def setup_method(self, method):
		
		#building sequence
		for i in range(1,7):
			self.positions.append(Position(i))
		self.sequence = PositionSequence(self.positions)
		
		#setting up robotController
		self.robotController = RobotController()
		#joing it together to build sequence executor
		self.sequenceExecutor = SequenceExecutor( self.robotController, self.sequence)
		
	def test_execute_goes_to_end(self):
		self.sequenceExecutor.executeOnce()
		
		assert self.sequenceExecutor.isOver() == True
	
	def test_execute_step_counter(self):
		self.sequenceExecutor.execute()
		
		assert self.robotController.getStepCount() == len(self.positions)
		
	def teardown_method(self, method):
		self.positions = []
		self.sequenceExecutor = 0
		self.robotController = 0