#Loading and intepreting file
#Author: Witold Wasilewski 2011

import os.path
from PositionLineInterpreter import PositionLineInterpreter
from PositionEncoder import PositionEncoder

class SequenceFileManager:
    
    def load( self, sequence, filename ):
        if os.path.exists(filename):
            #reading from file
            file = open(filename, "r")
            interpreter = PositionLineInterpreter()
            
            for line in file:
                if len(line) > 0:
                    interpreter.interpret( sequence, line )
                
            file.close()
        else:
            raise Exception("Filename not found")
        
        
    def save( self, sequence, filename ):
        file = open(filename, "w")
        
        if( sequence.amount() != 0 ):
            encoder = PositionEncoder()
            for i in range(0,sequence.amount()):
                encodedLine = encoder.encode(sequence.getPosition(i))
                file.write(encodedLine+"\n")
        
        file.close()