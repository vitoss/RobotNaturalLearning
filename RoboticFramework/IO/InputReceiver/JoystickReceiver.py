#Class responsible for receiving joystick based commands
#Author: Witold Wasilewski 2011

import pygame
from InputReceiver import InputReceiver 
import RoboticFramework.Position.DeltaJointPosition as DeltaJointPosition
import RoboticFramework.IO.PositionCommandLineInterpreter as PositionCommandLineInterpreter

class JoystickReceiver (InputReceiver):
    
    def __init__(self, threadID, name, _queue):
        InputReceiver.__init__(self, threadID, name, _queue)
        self.interpreter = PositionCommandLineInterpreter.PositionCommandLineInterpreter()
        #self.interpreter.concurentCommands = True
        
    def run(self):
        print "Starting " + self.customName
        pygame.init()
        
        #init joystick
        j = pygame.joystick.Joystick(0)
        j.init()
        print "Joystick " + j.get_name() + " initialized"
        
        #try:
        #master loop
        while True:
            
            if self.queue.full(): 
                continue #if queue is full ommit iteration
            
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
                        
            command = self.interpret_data(value)
            self.queue.put( command )
            
            del value

        #except:
         #  print "Unhandled error in joystick driver"
        
        print "Exiting " + self.customName
        
    def stop(self):
        #del self.interpreter
        print "Stop socket service"
        
    def interpret_data(self, data):
        axisScales = self.config.axisScales
        maxAxisValue = max(abs(data["axis1"]), abs(data["axis2"]), abs(data["axis3"]))
        speedFactor = maxAxisValue #self.config.speedFactor
        
        value = "moveBy("+ ('%1.1f' % (data["axis1"]*axisScales[0])) +", "+ ('%1.1f' % (data["axis2"]*axisScales[1])) +", "+ ('%1.1f' % (data["axis3"]*axisScales[2])) +", "+"0, 0, 0, "+('%f' % speedFactor)+")"
        print value
        return self.interpreter.interpretLine(value)
    
