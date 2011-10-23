import serial
import socket
import time

time.sleep(0.01)

#init socket
HOST, PORT = "127.0.0.1", 2007

# Create a socket (UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Connect to server and send data
sock.connect((HOST, PORT))
sock.setblocking(0)
sock.settimeout(1)

#init serial port
ser = serial.Serial("/dev/tty.usbserial-A400hDGp", 115200)

print ser.portstr
while True:
    i = 5
    mag = {}
    mag["x"] = 0
    mag["y"] = 0
    mag["z"] = 0
    
#    while i > 0: 
    line = ser.readline()
    line = line.strip()
    data = line.split(',')
    if len(data) != 10:
        print "Insufficient data"
        continue
    timestamp = data[0]
    mag["x"] += float(data[1])/45
    mag["y"] += float(data[2])/45
    mag["z"] += float(data[3])/45
       
    #i -= 1
        
    #mag["x"] /= 5
    #mag["y"] /= 5
    #mag["z"] /= 5
    mag["x"] += 45
    mag["y"] += 45
    
    command = "move("+("%.4f" % (mag["x"]))+","+("%.4f" % (mag["y"]))+","+("%.4f" % (mag["z"]))+", 0, 0, 0, 1)"
    print command
    sock.send(command)
    try:
        print sock.recv(1024)
    except Exception:
        continue
    
    time.sleep(0)
    
ser.close()
sock.close()

#Functions
#mag = 1/45
#acc = 1/4096*3300/400*9.81*0.9387   [-1 1 1]
#gyro = 1/4096*3300*PI/180    [-1 1 1]