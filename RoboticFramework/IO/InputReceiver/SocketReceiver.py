#Class responsible for receiving socket based commands
#Author: Witold Wasilewski 2011

import SocketServer
from InputReceiver import InputReceiver 
import RoboticFramework.Position.DeltaJointPosition as DeltaJointPosition
import RoboticFramework.IO.PositionCommandLineInterpreter as PositionCommandLineInterpreter
from RoboticFramework.IO.RecordingInterpreter import RecordingInterpreter

class SocketReceiver (InputReceiver):
    
    
    def run(self):
        
        print "Starting " + self.customName
        
        SocketReceiverHandler.queue = self.queue
        
        HOST, PORT = self.config.ip, self.config.port
        SocketServer.UDPServer.allow_reuse_address = True
        self.server = SocketServer.UDPServer((HOST, PORT), SocketReceiverHandler)
        self.server.serve_forever()
		
        print "Exiting " + self.customName
        
    def stop(self):
        print "Stop socket service"
        self.server.shutdown()

        

class SocketReceiverHandler(SocketServer.BaseRequestHandler):
    
    def setup(self):
        self.positionInterpreter = PositionCommandLineInterpreter.PositionCommandLineInterpreter()
        self.positionInterpreter.concurentCommands = True
        self.recordingInterpreter = RecordingInterpreter()
        SocketServer.BaseRequestHandler.setup(self)
    
    def finish(self):
        del self.positionInterpreter
        del self.recordingInterpreter
        SocketServer.BaseRequestHandler.finish(self)
        
    def handle(self):
        
        socket = self.request[1]
        messageCounter = self.queue.qsize()
        socket.sendto(str(messageCounter).encode('ascii')+"\n", self.client_address)
        
        if self.queue.full():
            return #if queue is full: quit
        
        data = self.request[0].strip()
        
        print "%s wrote:" % self.client_address[0]
        print data
        
        command = self.interpret_absolute(data)
        self.queue.put( command )
        
    def interpret_absolute(self, data):
        attempt = self.positionInterpreter.interpret(data)
        if( attempt == -1 ):
            attempt = self.recordingInterpreter.interpret(data)
        
        return attempt