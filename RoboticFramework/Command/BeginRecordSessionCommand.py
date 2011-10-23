#BeginRecordSessionCommand
#Author: Witold Wasilewski 2011

from Command import Command

class BeginRecordSessionCommand(Command):
    
    def execute(self, robotController):
        robotController.startRecordSession()