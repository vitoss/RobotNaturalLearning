#Test for line interpreter
#Author: Witold Wasilewski 2011

from RoboticFramework.IO.PositionLineInterpreter import PositionLineInterpreter
from RoboticFramework.Position.PositionSequence import PositionSequence

class TestLineIntepreter:
	
	def setup_method(self, method):
		self.interpreter = PositionLineInterpreter()
		self.sequence = PositionSequence([])
		
	def test_simpleJoint(self):
		self.interpreter.interpret(self.sequence, "move(60.0,-30.0,30.0,-20.0,10.0,-40.0)")
		
		assert self.sequence.amount() == 1
		assert self.sequence.getCurrentPosition().getValue()[1] == -30
	
	def test_comments(self):
		self.interpreter.interpret(self.sequence, "#testing line")
		
		assert self.sequence.amount() == 0
		
	def test_newline(self):
		self.interpreter.interpret(self.sequence, " \n")
		
		assert self.sequence.amount() == 0
	
	def test_cartesianLine(self):
		self.interpreter.interpret(self.sequence, "moveCartesian(60.0,-30.0,30.0)")
		
		assert self.sequence.amount() == 1
		assert self.sequence.getCurrentPosition().type == "Cartesian"
		
	def test_deltaJointLine(self):
		self.interpreter.interpret(self.sequence, "moveBy(60.0,-30.0,30.0,3,3,3)")
		
		assert self.sequence.amount() == 1
		assert self.sequence.getCurrentPosition().type == "DeltaJoint"
	
	def test_deltaCartesianLine(self):
		self.interpreter.interpret(self.sequence, "moveCartesianBy(60.0,-30.0,30.0)")
		
		assert self.sequence.amount() == 1
		assert self.sequence.getCurrentPosition().type == "DeltaCartesian"
	
	def teardown_method(self, method):
		self.interpreter = 0
		self.sequence = 0
		