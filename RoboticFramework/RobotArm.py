#Generic Robot Arm class.
#6 axis
#Author: Witold Wasilewski 2011

class RobotArm:
    JointPositions = [] #current state of joints
    
    #private
    _JointIncerements = [] #how much we incement, speed
    _JointTargetPosition = [] #where we're heading
    _Constrainments = [] #where we can move
    _JointMaxSpeed = []
    
    def __init__( self, zeroPosition, constrainments, maxSpeed ):
        self.JointPositions = list(zeroPosition)
        self._Constrainments = list(constrainments)
        self._JointMaxSpeed = list(maxSpeed)
        self._JointTargetPosition = list(zeroPosition) #copy array of zeros position
        self._JointIncerements = list(zeroPosition)
        self.speedFactor = 1 #float 0-1, limiting speed
    
    def rotateTo( self, jointNumber, degree ):
        if jointNumber >= len(self.JointPositions):
            raise Exception( "There are no such Joint" )
    
        if abs( self.JointPositions[jointNumber] - degree ) < 1 :
            return # we are already there
            
        #checking if we can make move
        minAxisConstr = self._Constrainments[jointNumber][0]
        maxAxisConstr = self._Constrainments[jointNumber][1];

        if minAxisConstr > degree or maxAxisConstr < degree :
            return -1
        
        self._JointTargetPosition[jointNumber] = degree
        #we assume full speed when rotating only one joint
        self._JointIncerements[jointNumber] = (self._JointTargetPosition[jointNumber] - self.JointPositions[jointNumber])*self._JointMaxSpeed[jointNumber]*self.speedFactor/360;
        print self._JointIncerements[jointNumber]
        
    def rotateBy( self, jointNumber, byDegree ):
        if jointNumber >= len(self.JointPositions):
            raise Exception( "There are no such Joint" )
        
        #checking if we can make move
        minAxisConstr = self._Constrainments[jointNumber][0]
        maxAxisConstr = self._Constrainments[jointNumber][1];

        degree = self.JointPositions[jointNumber] + byDegree
        
        if minAxisConstr > degree or maxAxisConstr < degree :
            return -1
            
        self._JointTargetPosition[jointNumber] = degree
        #we assume full speed when rotating only one joint
        self._JointIncerements[jointNumber] = (self._JointTargetPosition[jointNumber] - self.JointPositions[jointNumber])*self._JointMaxSpeed[jointNumber]*self.speedFactor/360.0;
        
    
    def isRotateDone( self, jointNumber ):
        if abs(self.JointPositions[jointNumber] - self._JointTargetPosition[jointNumber]) < 1:
            self.JointPositions[jointNumber] = self._JointTargetPosition[jointNumber]
            return True
        else:
            return False
    
    def isMovementDone(self):
        for i in range(0,len(self.JointPositions)):
            if self.isRotateDone(i) == False:
                return False
        
        return True
    
    
    def makeMove( self ):
        for i in range(0,6):
            if self._JointIncerements[i] != 0:
                if abs(self._JointTargetPosition[i] - self.JointPositions[i]) < self._JointIncerements[i]:
                    self.JointPositions[i] = self._JointTargetPosition[i]
                else:
                    self.JointPositions[i] += self._JointIncerements[i]
                
            #resetting incerements when achiving target position
            if self.isRotateDone( i ) == True:
                self._JointIncerements[i] = 0

    def getJointAmount(self):
        return len(self.JointPositions)
    
    def setSpeedFactor( self, _speedFactor ):
        if _speedFactor > 1:
            _speedFactor = 1
        elif _speedFactor < 0:
            _speedFactor = 0
         
        self.speedFactor = _speedFactor
        