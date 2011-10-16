#Command for command loop
#Author: Witold Wasilewski 

import Command

class CommandLoop (Command.Command):

    #command
    #counter

    def __init__(self):
        Command.Command.__init__(self)
        self.command = -1
        self.counter = 0
    
    def execute(self, robotController):
        i = self.counter
        while i > 0:
            i = i -1
            self.command.execute(robotController)