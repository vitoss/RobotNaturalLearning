#StopRecordCommand
#Author: Witold Wasilewski 2011

from Command import Command

class StopRecordCommand(Command):
    
    def execute(self, robotController):
        robotController.stopRecording()