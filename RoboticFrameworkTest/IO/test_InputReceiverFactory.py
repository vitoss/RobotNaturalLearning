#Testing sequence file manager
#Author: Witold Wasilewski

from RoboticFramework.IO.InputReceiverFactory import InputReceiverFactory
from RoboticFramework.IO.InputReceiver.KeyboardReceiver import KeyboardReceiver
from RoboticFramework.IO.InputReceiver.SocketReceiver import SocketReceiver
from config import Config
import os.path
import py.test
import Queue

class TestInputReceiverFactory:
    
    def setup_method(self, method):
        configFile = "settings.cfg"
        self.config = Config( configFile )
        
        queue = Queue.Queue(maxsize=0)
        self.factory = InputReceiverFactory(queue, self.config)
            
    def test_createKeyboard_simple(self):
        receiver = self.factory.createKeyboard()
        assert receiver.__class__ == KeyboardReceiver
        assert receiver.config == self.config.Keyboard
    
    def test_createSocket_simple(self):
        receiver = self.factory.createSocket()
        assert receiver.__class__ == SocketReceiver
        assert receiver.config == self.config.Sockets.Simple
            
    def teardown_method(self, method):
        del self.config
        del self.factory