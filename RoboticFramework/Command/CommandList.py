#Command list
#Author: Witold Wasilewski 2011

import Command

class CommandList (Command.Command):
    
    def __init__(self):
        self.commands = []
    
    def execute(self, robotController):
        if len(self.commands) == 0:
            return True
         
        for i in range(0, len(self.commands)):
            self.commands[i].execute(robotController)
        
        return True
    
    
    def add( self, command ):
        self.commands.append(command)