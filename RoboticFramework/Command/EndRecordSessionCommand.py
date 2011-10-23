#EndRecordSessionCommand
#Author: Witold Wasilewski 2011

from Command import Command

class EndRecordSessionCommand(Command):
    
    def execute(self, robotController):
        robotController.stopRecordSession()