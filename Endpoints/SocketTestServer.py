#Class responsible for receiving socket based commands
#Author: Witold Wasilewski 2011

import time
import SocketServer

class SocketReceiverHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print "%s wrote:" % self.client_address[0]
        print data
        socket.sendto(data.upper(), self.client_address)
        
HOST, PORT = "192.168.0.104", 2006
server = SocketServer.UDPServer((HOST, PORT), SocketReceiverHandler)
server.serve_forever()

        


      