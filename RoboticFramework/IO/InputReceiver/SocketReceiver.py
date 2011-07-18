#Class responsible for receiving socket based commands
#Author: Witold Wasilewski 2011

import time
import SocketServer
from InputReceiver import InputReceiver 
import RoboticFramework.Position.DeltaJointPosition as DeltaJointPosition
import RoboticFramework.IO.PositionLineInterpreter as PositionLineInterpreter

class SocketReceiver (InputReceiver):
    
    
    def run(self):
        
        print "Starting " + self.customName
        
        SocketReceiverHandler.queue = self.queue
        
        HOST, PORT = self.config.ip, self.config.port
        self.server = SocketServer.UDPServer((HOST, PORT), SocketReceiverHandler)
        self.server.serve_forever()
		
        print "Exiting " + self.customName
        
    def stop(self):
        print "Stop socket service"
        self.server.shutdown()

        

class SocketReceiverHandler(SocketServer.BaseRequestHandler):
    
    def setup(self):
        self.interpreter = PositionLineInterpreter.PositionLineInterpreter()
        SocketServer.BaseRequestHandler.setup(self)
    
    def finish(self):
        del self.interpreter
        SocketServer.BaseRequestHandler.finish(self)
        
    def handle(self):
        
        if self.queue.full(): 
            return #if queue is full quit
        
        #self.queue.put(DeltaJointPosition.DeltaJointPosition([5,5,5,5,5,5]))
        data = self.request[0].strip()
        socket = self.request[1]
        print "%s wrote:" % self.client_address[0]
        print data
        socket.sendto(data.upper(), self.client_address)
        
        command = self.interpret_absolute(data)
        self.queue.put( command )
        
    def interpret_absolute(self, data):
        return self.interpreter.interpretLine(data)