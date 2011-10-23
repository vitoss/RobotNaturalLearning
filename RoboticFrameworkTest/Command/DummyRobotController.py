#Dummy robot controller
#Author: Witold Wasilewski

class DummyRobotController:
    
    def __init__(self):
        self.isRecording = False
        self.isSessionRecordingActive = False
        self.isRecordingActive = False
        
    def startRecordSession(self):
        self.isSessionRecordingActive = True

    def stopRecordSession(self):
        self.isSessionRecordingActive = False
        
    def startRecording(self):
        self.isRecording = True
    
    def stopRecording(self):
        self.isRecording = False