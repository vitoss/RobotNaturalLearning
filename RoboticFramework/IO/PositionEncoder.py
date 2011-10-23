#Position encoder
#Author: Witold Wasilewski 2011

class PositionEncoder:
    
    def encode(self, position):
        if( position.type == "Joint" ):
            functionName = "move"
        elif( position.type == "DeltaJoint" ):
            functionName = "moveBy"
            
        return functionName + "("+ ','.join(["%s" % j for j in position.getValue()]) +")"