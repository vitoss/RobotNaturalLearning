#Testing position encoder
#Author: Witold Wasilewski 2011

from RoboticFramework.IO.PositionEncoder import PositionEncoder
from RoboticFramework.Position.JointPosition import JointPosition
from RoboticFramework.Position.DeltaJointPosition import DeltaJointPosition


class TestPositionEncoder:
    def setup_method(self, method):
        self.encoder = PositionEncoder()
        
    def test_simpleJoint_simple(self):
        position = JointPosition([10,10,10,10,10,10])
        
        line = self.encoder.encode(position)
        assert line == "move(10,10,10,10,10,10)"
    
    def test_simpleJoint_speedFactor(self):
        position = JointPosition([10,10,10,10,10,10,1])

        line = self.encoder.encode(position)
        assert line == "move(10,10,10,10,10,10,1)"

    def test_deltaJoint_simple(self):
         position = DeltaJointPosition([10,10,10,10,10,10])

         line = self.encoder.encode(position)
         assert line == "moveBy(10,10,10,10,10,10)"

    def test_deltaJoint_speedFactor(self):
         position = DeltaJointPosition([10,10,10,10,10,10,1])

         line = self.encoder.encode(position)
         assert line == "moveBy(10,10,10,10,10,10,1)", "Wrong delta joint encoding with speed factor"
        
    def teardown_method(self, method):
        del self.encoder