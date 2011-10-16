import cmd2

class RobotWorld(cmd2.Cmd):
    """Robot command processor."""
    
    prompt = "(robot):"
    intro = "Welcome in robot arm simulator"
    echo = False
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
    
    def do_EOF(self, line):
        return True
        
