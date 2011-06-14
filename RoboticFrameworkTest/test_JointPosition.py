#Test for JointPosition
#Author: Witold Wasilewski 2011

from RoboticFramework.Position.JointPosition import JointPosition

class TestJointPosition:
	
	def test_init(self):
		position = JointPosition([1,2,3,4,5,6])
		
		assert position.getValue()[2] == 3
	
	def test_array(self):
		positions = []
		for i in range(0,4):
			positions.append( JointPosition([1*i, 2*i, 3*i, 4*i, 5*i]))
		
		assert positions[2].getValue()[1] == 4
	
	def test_copy_array(self):
		#making positions
		positions = []
		for i in range(0,4):
			positions.append( JointPosition([1*i, 2*i, 3*i, 4*i, 5*i]))
		
		#copy
		positions2 = list(positions)
		
		assert positions2[2].getValue()[1] == 4
		