#Console endpoint, for intractive use with robot!
#Author Witold Wasilewski 2011

import socket
from RobotWorld import RobotWorld

#configuration
port_address = "127.0.0.1"
port_number = 2007

#init phase
# Create a socket (UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect to server and send data
sock.connect((port_address, port_number))

#init cmd
if __name__ == '__main__':
    console = RobotWorld()
    console.sock = sock
    console.cmdloop()
    
#cleanup
sock.close()
