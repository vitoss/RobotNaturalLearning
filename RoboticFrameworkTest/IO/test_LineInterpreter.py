#Test for line interpreter
#Author: Witold Wasilewski 2011

from RoboticFramework.IO.LineInterpreter import LineInterpreter
from RoboticFramework.Position.PositionSequence import PositionSequence

class TestLineIntepreter:
	
	def setup_method(self, method):
		self.interpreter = LineInterpreter()
		self.sequence = PositionSequence([])
		
	def test_simpleJoint(self):
		self.interpreter.interpret(self.sequence, "60.0,-30.0,30.0,-20.0,10.0,-40.0 ")
		
		assert self.sequence.amount() == 1
		assert self.sequence.getCurrentPosition().getValue()[1] == -30
	
	def teardown_method(self, method):
		self.interpreter = 0
		self.sequence = 0
		