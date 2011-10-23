#Fake socket client
#Author: Witold Wasilewski 2011

from RoboticFramework.IO.InputReceiver.SocketReceiver import SocketReceiver
import Queue
from RoboticFramework.IO.InputReceiverManager import InputReceiverManager
from RoboticFramework.IO.InputReceiverFactory import InputReceiverFactory
from config import Config

configFile = "../../settings.cfg"
config = Config( configFile )
queue = Queue.Queue(maxsize=config.queueMaxSize)
inputReceiversManager = InputReceiverManager()
inputReceiversFactory = InputReceiverFactory(queue, config)

inputReceiversManager.add(inputReceiversFactory.createSocket())

inputReceiversManager.start()

raw_input("Press Enter to continue...")