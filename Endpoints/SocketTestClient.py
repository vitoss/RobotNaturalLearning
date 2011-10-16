import socket
import sys
import time

HOST, PORT = "192.168.0.104", 2006
data = " ".join(sys.argv[1:])

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().

sock.sendto(data + "\n", (HOST, PORT))
received = sock.recv(1024)

    
#i = 0
#while( i < 10 ):
#    position = 5*i
#    data = "move("+str(position)+","+str(position)+","+str(position)+","+str(position)+","+str(position)+","+str(position)+")"
#    sock.sendto(data + "\n", (HOST, PORT))
#    received = sock.recv(1024)
#    i = i+1
#    time.sleep(0.5)

print "Sent:     %s" % data
print "Received: %s" % received