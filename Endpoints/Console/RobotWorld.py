import cmd2

class RobotWorld(cmd2.Cmd):
    """Robot command processor."""
    
    prompt = "(robot):"
    intro = "Welcome in robot arm simulator"
    echo = True
    timing = False
    debug = True
    
    def do_move(self, arg):
        position = arg.split(',')
        
        if len(position) < 6:
            print "Position should has at least 6 parameters."
            return
        if len(position) > 7:
            print "Too many attributes."
            return
            
        command = "move("+arg+")\n"

        self.sock.send(command) #sending command
        print self.sock.recv(1024) #printing response
    
    def help_move(self):
        print '\n'.join([ 'move [position],[speedFactor]',
                           'Move robot arm to absolute position.',
                           'Position is 6 element array.',
                                   ])
                                   
    def do_move2(self, arg):
        position = arg.split(',')
        position = [float(i) for i in position]
        
        if len(position) < 6:
            print "Position should has at least 6 parameters."
            return
        if len(position) > 7:
            print "Too many attributes."
            return
            
        import struct
        if len(position) == 6:
            command = struct.pack("!dffffff", 1, position[0],position[1],position[2],position[3],position[4],position[5] )
        elif len(position) == 7:
            command = struct.pack("!dfffffff", 2, position[0],position[1],position[2],position[3],position[4],position[5],position[6])
        
        self.sock.send(command+"\n")
        print self.sock.recv(1024)
    
    def do_beginrecordsession(self, arg):
        command = "BeginRecordSession()\n"
        self.sock.send(command)
        print self.sock.recv(1024)
    
    def do_endrecordsession(self, arg):
        command = "EndRecordSession()\n"
        self.sock.send(command)
        print self.sock.recv(1024)

    def do_startrecording(self, arg):
        command = "StartRecording()\n"
        self.sock.send(command)
        print self.sock.recv(1024)   
    
    def do_stoprecording(self, arg):
        command = "StopRecording()\n"
        self.sock.send(command)
        print self.sock.recv(1024)  
        
    def do_sleep(self, arg):
        import time
        time.sleep(float(arg)) 
    
    def do_EOF(self, line):
        return True
        
