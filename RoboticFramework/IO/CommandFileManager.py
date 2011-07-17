#Loading and intepreting file
#Author: Witold Wasilewski 2011

import os.path
import CommandLineInterpreter
import RoboticFramework.Command.CommandList as CommandList
reload(CommandLineInterpreter)

class CommandFileManager:
    
    def load( self, filename ):
        if os.path.exists(filename):
            #reading from file
            file = open(filename, "r")
            interpreter = CommandLineInterpreter.CommandLineInterpreter(CommandList.CommandList())
            
            for line in file:
                if len(line) > 0:
                    interpreter.interpret( line )
                
            file.close()
            
            return interpreter.currentList
        else:
            raise Exception("Filename not found")
        
        
    def save( self, sequence, filename ):
        file = open(filename, "w")
        #
        # TODO
        #
        file.close()