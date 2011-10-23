import socket
import sys
import pygame
import time

def start():
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    print j.get_name()
    
    HOST, PORT = "127.0.0.1", 2007

    # Create a socket (UDP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setblocking(0)
    sock.settimeout(5)
    
    # Connect to server and send data
    sock.connect((HOST, PORT))

    try:
        while True:
            value = {}
            pygame.event.pump()
            
            isDataSetEmpty = True
            
            #axis
            for i in range(3):
                axisValue = j.get_axis(i)
                value["axis%d" % (i+1)] = axisValue
                if axisValue != 0:
                    isDataSetEmpty = False
                
            #buttons    
            for i in range(11):
                buttonValue = j.get_button(i)
                value["button%d" % (i+1)] = buttonValue
                if buttonValue != 0:
                    isDataSetEmpty = False
             
            if isDataSetEmpty: 
                continue
            
            axisScales = [8,8,8] #TODO from config?
            maxAxisValue = max(abs(value["axis1"]), abs(value["axis2"]), abs(value["axis3"]))
            speedFactor = maxAxisValue #self.config.speedFactor
            
            tempstr = "moveBy("+ ('%1.1f' % (value["axis1"]*axisScales[0])) +", "+ ('%1.1f' % (value["axis2"]*axisScales[1])) +", "+ ('%1.1f' % (value["axis3"]*axisScales[2])) +", "+"0, 0, 0, "+('%f' % speedFactor)+")"
            
            sock.send(tempstr + "\n")
            
            # Receive data from the server and shut down
            received = sock.recv(1024)

            print "Sent:     %s" % tempstr
            print "Received: %s" % received
                
            del tempstr
            del value
                
            time.sleep(0.1)

    except Exception as ex:
        print ex
        print "closing"
    
    sock.close()

if __name__ == '__main__':
    start()