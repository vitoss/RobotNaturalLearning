#Delta axis joint - it holds delta value for one axis - with reference to previous position
#Author: Witold Wasilewski 2011

from Position import Position

class AxisDeltaJointPosition ( Position ):
	type = "AxisDeltaJoint"
	
	