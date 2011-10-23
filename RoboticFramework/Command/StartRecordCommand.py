#StarRecordCommand
#Author: Witold Wasilewski 2011

from Command import Command

class StartRecordCommand(Command):
    
    def execute(self, robotController):
        robotController.startRecording()