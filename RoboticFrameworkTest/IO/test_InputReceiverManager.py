#Testing sequence file manager
#Author: Witold Wasilewski

from RoboticFramework.IO.InputReceiverManager import InputReceiverManager
from RoboticFramework.IO.InputReceiverFactory import InputReceiverFactory
from RoboticFramework.IO.InputReceiver.KeyboardReceiver import KeyboardReceiver
from RoboticFramework.IO.InputReceiver.SocketReceiver import SocketReceiver
from RoboticFrameworkTest.IO.InputReceiver.KeyboardReceiverMock import KeyboardReceiverMock
from config import Config
import os.path
import py.test
import Queue

class TestInputReceiverManager:
    
    def setup_method(self, method):
        configFile = "settings.cfg"
        self.config = Config( configFile )
        
        queue = Queue.Queue(maxsize=0)
        self.factory = InputReceiverFactory(queue, self.config)
        self.manager = InputReceiverManager()
            
    def test_add_simple(self):
        receiver = KeyboardReceiverMock(1, "sample", self.config)
        self.manager.add(receiver)
        assert self.manager.has(receiver)
    
    def test_remove_simple(self):
        receiver = KeyboardReceiverMock(1, "sample", self.config)
        self.manager.add(receiver)
        self.manager.remove(receiver)
        assert not self.manager.has(receiver)
    
    def test_start_simple(self):
        receiver = KeyboardReceiverMock(1, "sample", self.config)
        self.manager.add(receiver)
        assert not receiver.isStarted
        self.manager.start()
        assert receiver.isStarted
    
    def test_stop_simple(self):
        receiver = KeyboardReceiverMock(1, "sample", self.config)
        self.manager.add(receiver)
        self.manager.start()
        self.manager.stop()
        assert not receiver.isStarted
                
    def teardown_method(self, method):
        del self.config
        del self.manager
        del self.factory