#Generic Robot Arm class.
#6 axis
#Author: Witold Wasilewski 2011

import time

class RobotArm:
    JointPositions = [] #current state of joints
    
    #private
    _JointIncrements = [] #how much we incement, speed
    _JointTargetPosition = [] #where we're heading
    _Constrainments = [] #where we can move
    _JointMaxSpeed = []
    
    def __init__( self, zeroPosition, constrainments, maxSpeed, accuracy ):
        self.JointPositions = list(zeroPosition)
        self._Constrainments = list(constrainments)
        self._JointMaxSpeed = list(maxSpeed)
        self._JointTargetPosition = list(zeroPosition) #copy array of zeros position
        self._JointIncrements = list(zeroPosition)
        self.speedFactor = 1 #float 0-1, limiting speed
        self.accuracy = accuracy
    
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
        self._JointIncrements[jointNumber] = (self._JointTargetPosition[jointNumber] - self.JointPositions[jointNumber])*self._JointMaxSpeed[jointNumber]*self.speedFactor/360.0;
        
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
        positionDifference = self._JointTargetPosition[jointNumber] - self.JointPositions[jointNumber]
            
        self._JointIncrements[jointNumber] = positionDifference*self._JointMaxSpeed[jointNumber]*self.speedFactor/100.0;
        if abs(self._JointIncrements[jointNumber]) < self.accuracy*20:
            if self._JointIncrements[jointNumber] >= 0 :
                self._JointIncrements[jointNumber]  = self.accuracy*20
            else:
                self._JointIncrements[jointNumber] = -self.accuracy*20
    
    def isRotateDone( self, jointNumber ):
        if abs(self.JointPositions[jointNumber] - self._JointTargetPosition[jointNumber]) <= self.accuracy:
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
        for i in range(0,len(self.JointPositions)):
            if self._JointIncrements[i] != 0:
                if abs(self._JointTargetPosition[i] - self.JointPositions[i]) <= abs(self._JointIncrements[i]):
                    self.JointPositions[i] = self._JointTargetPosition[i]
                else:
                    self.JointPositions[i] += self._JointIncrements[i]
                
                #resetting incerements when achiving target position
                if self.isRotateDone( i ) == True:
                    self._JointIncrements[i] = 0
                    
            elif self.isRotateDone( i ) == False:
                raise Exception("Joints consistancy fail")
                
        #time.sleep(0.0005)

    def getJointAmount(self):
        return len(self.JointPositions)
    
    def setSpeedFactor( self, _speedFactor ):
        if _speedFactor > 1:
            _speedFactor = 1
        elif _speedFactor < 0:
            _speedFactor = 0
         
        self.speedFactor = _speedFactor
    
    def stopAtCurrentPosition(self):
        if self.isMovementDone():
            #do nothing
            pass
        else:
            #reset
            for i in range(0, self.getJointAmount()):
                self._JointTargetPosition[i] = self.JointPositions[i]
                self._JointIncrements[i] = 0
                
        
        