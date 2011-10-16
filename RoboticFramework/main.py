# Robot animation main script
# Author: Witold Wasilewski 2011
# Should be fired from blender

from Blender import *  
from Blender import Mathutils as Math
from Blender.Mathutils import Matrix
from math import *

#modules
import RoboticFramework
from RoboticFramework import RobotArm
from RoboticFramework import RobotModelBounder
from RoboticFramework import RobotController
from RoboticFramework.Position import JointPosition 
import RoboticFramework.IO.CommandFileManager as CommandFileManager

#Blender runs in one python instance, so we need reload this when developing
reload(RobotArm)
reload(RobotModelBounder)
reload(RobotController)
reload(CommandFileManager)

#Input receivers libraries
import Queue
import pygame

from RoboticFramework.IO.InputReceiverManager import InputReceiverManager
reload (RoboticFramework.IO.InputReceiverManager )
from RoboticFramework.IO.InputReceiverFactory import InputReceiverFactory
reload (RoboticFramework.IO.InputReceiverFactory )

pygame.init()

#

links = []
links.append( Object.Get('linkone') ) 
links.append( Object.Get('linktwo') )         
links.append( Object.Get('linkthree') )
links.append( Object.Get('linkfour') )          
links.append( Object.Get('linkfive') )          
links.append( Object.Get('linksix') )

tool= Object.Get('tool')           
toolPiston= Object.Get('toolpiston')

#init Robot Arm abstract model
initPositions = [0,0,0,0,0,0]
constrainments = [[0,100],[0,100],[0,100],[0,100],[0,100],[0,100]]
maxSpeed = [10,10,10,10,10,10]

robotArm = RobotArm.RobotArm( initPositions, constrainments, maxSpeed )

#init model bounder
robotModelBounder = RobotModelBounder.RobotModelBounder( robotArm, links, tool, toolPiston )

#setup robotController
robotController = RobotController.RobotController(robotArm, robotModelBounder, Redraw )


#reading from file
manager = CommandFileManager.CommandFileManager()
#manager.load(sequence, "/Users/vito/Dropbox/Projects/bch/fanuc-LR-Mate200i-simulation/angles.txt")
commands = manager.load("D:/My Dropbox/Projects/bch/RobotLearning/commands.txt")

commands.execute(robotController)

#Input Receivers
#create queue for input events. Maxsize set to 0 means unlimited number of events
queue = Queue.Queue(maxsize=0)

inputReceiversManager = InputReceiverManager()
inputReceiversFactory = InputReceiverFactory(queue)

inputReceiversManager.add(inputReceiversFactory.createSocket())
inputReceiversManager.add(inputReceiversFactory.createJoystick())
inputReceiversManager.start()

robotController.startProcessingInputQueue(queue)