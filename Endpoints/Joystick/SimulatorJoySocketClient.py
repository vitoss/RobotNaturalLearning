
import socket
import sys
import time

def start():
    HOST, PORT = "127.0.0.1", 2007

    # Create a socket (UDP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setblocking(0)
    sock.settimeout(5)
    
    # Connect to server and send data
    sock.connect((HOST, PORT))
    
    interval = 0.01
    lastQueue = 0
    loopsSinceLastRejection = 0
    loopBoundry = 100
    lastRejectedInterval = 0
    try:
        i = 10
        while True:
            i = i*(-1)
            loopsSinceLastRejection = loopsSinceLastRejection + 1
            value = {}
            inc = str(i);
            tempstr = "moveBy("+inc+","+inc+","+inc+","+inc+","+inc+","+inc+",1)\n"
           
            
            sock.send(tempstr.encode('ascii'))
            
            # Receive data from the server and shut down
            received = sock.recv(1024)
            
            # we want real time system
            queueCounter = int(received)
            if( lastQueue <= queueCounter and queueCounter != 0 ):
                #we need to send slowly
                if( lastRejectedInterval == interval ):
                    loopBoundry = loopBoundry*2
                    lastRejectedInterval = interval
                else:
                    loopBoundry = 100
                    
                if( interval < 1 ):
                    interval = interval + 0.01
            elif( queueCounter == 0 and loopsSinceLastRejection >= loopBoundry ):
                
                loopsSinceLastRejection = 0
                
                if( interval > 0.01 ):
                    interval = interval - 0.01
                    
            lastQueue = queueCounter

            print "Sent:     %s" % tempstr
            print "Received: %s" % received
            print "CurrentInterval: %f" % interval
            
            del tempstr
            del value
                
            time.sleep(interval)

    except Exception as ex:
        print ex
        print "closing"
    
    sock.close()

if __name__ == '__main__':
    start()