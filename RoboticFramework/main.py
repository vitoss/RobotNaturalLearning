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
from RoboticFramework.Position.PositionSequence import PositionSequence
from RoboticFramework.Position.JointPosition import JointPosition
from RoboticFramework.SequenceExecutor import SequenceExecutor
from RoboticFramework.IO.SequenceFileManager import SequenceFileManager

#Blender runs in one python instance, so we need reload this when developing
reload(RobotArm)
reload(RobotModelBounder)
reload(RobotController)
reload(JointPosition)

#
reload(RoboticFramework.SequenceExecutor)

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


#Building positionSequence
#positions = []
#positions.append(JointPosition( [60.0,-30.0,30.0,-20.0,10.0,-40.0] ))
#positions.append(JointPosition( [-80.0,30.0,-30.0,20.0,-10.0,40.0] ))
#positions.append(JointPosition( [0.0,-45.0,45.0,0.0,20.0,0.0] ))
#sequence = PositionSequence(positions)

#reading from file
sequence = PositionSequence()
manager = SequenceFileManager()
manager.load(sequence, "angles.txt")

#setup sequenceExecutor
#sequenceExecutor = SequenceExecutor(robotController, sequence)
#sequenceExecutor.execute(2)
