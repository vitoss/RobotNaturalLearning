#Helper class to create receivers. Load configuration. 
#Author: Witold Wasilewski

import InputReceiver.KeyboardReceiver as KeyboardReceiver
import InputReceiver.SocketReceiver as SocketReceiver
#import InputReceiver.JoystickReceiver as JoystickReceiver
reload( KeyboardReceiver )
reload( SocketReceiver )
#reload( JoystickReceiver )

class InputReceiverFactory:
    
    def __init__(self, _queue, _config):
        self.queue = _queue
        self.config = _config
    
    def createKeyboard(self):
        print "Creating keyboard"
        newReceiver = KeyboardReceiver.KeyboardReceiver( 1, "Keyboard", self.queue)
        newReceiver.config = self.config.Keyboard
        newReceiver.start()
        return newReceiver
        
    def createSocket(self):
        print "Creating socket"
        newReceiver = SocketReceiver.SocketReceiver( 2, "Socket", self.queue )
        newReceiver.config = self.config.Sockets.Simple #iPhone
        newReceiver.start()
        return newReceiver
    
#    def createJoystick(self):
#        print "Creating joystick"
#        newReceiver = JoystickReceiver.JoystickReceiver( 3, "Joystick", self.queue )
#        newReceiver.config = self.config.Joystick
#        newReceiver.start()
#        return newReceiver