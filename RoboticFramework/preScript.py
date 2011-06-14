#### authors-Amit Raj Thatipalli & Raymond Asa Manis 
#### "Copyright 2010 Amit Raj Thatipalli"
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from Blender import *  
from Blender import Mathutils as Math
from Blender.Mathutils import Matrix
from math import *

# Disabled right know becouse of problems with compiler
#try:
#	import psyco
#	psyco.full()
#except:
#	print 'For optimal performance on an x86 CPU, install psyco'

#Get Links
linkone= Object.Get('linkone')           
linktwo= Object.Get('linktwo')          
linkthree= Object.Get('linkthree')          
linkfour= Object.Get('linkfour')          
linkfive= Object.Get('linkfive')           
linksix= Object.Get('linksix')           

tool= Object.Get('tool')           

toolpiston= Object.Get('toolpiston')           

######initializing###############

#thetas are current state of the arm
theta1=0.0
theta2=0.0
theta3=0.0
theta4=0.0
theta5=0.0
theta6=0.0

theta1_list=[]
theta2_list=[]
theta3_list=[]
theta4_list=[]
theta5_list=[]
theta6_list=[]


#Loading from file
for line in open("/Users/vito/Downloads/blender-2.49b-OSX-10.5-py2.5-intel/fanuc-LR-Mate200i-simulation/angles.txt", 'r'): ## opens the text file which in the same forlder if the text file is in difrent folder give the path to it example:'C:\\path to\\angles.txt'
    theta1,theta2,theta3,theta4,theta5,theta6 = map( float, line.split(","))
    theta1_list.append(theta1)
    theta2_list.append(theta2)
    theta3_list.append(theta3)
    theta4_list.append(theta4)
    theta5_list.append(theta5)
    theta6_list.append(theta6)

#
	#####find the max angle of the six angles
    find_maxangle=[theta1,theta2,theta3,theta4,theta5,theta6] 
    for angle in find_maxangle:
      if angle<0:
         if (angle*-1)>max_angle:
           global max_angle
           max_angle=-angle
      else:
         if angle>max_angle:
           global max_angle
           max_angle=angle


####simulation loop#####
for j in range(0,len(theta1_list),1):
    if j is 0:
       theta1=float(theta1_list[j]/max_angle)
       theta2=float(theta2_list[j]/max_angle)
       theta3=float(theta3_list[j]/max_angle)
       theta4=float(theta4_list[j]/max_angle)
       theta5=float(theta5_list[j]/max_angle)
       theta6=float(theta6_list[j]/max_angle)

	#theta_inc are incremental change for every move
    theta1_inc=float(theta1_list[j]/max_angle)    
    theta2_inc=float(theta2_list[j]/max_angle)
    theta3_inc=float(theta3_list[j]/max_angle)
    theta4_inc=float(theta4_list[j]/max_angle)
    theta5_inc=float(theta5_list[j]/max_angle)
    theta6_inc=float(theta6_list[j]/max_angle)



    for i in range (0 ,  int(max_angle) , 1):                      
               linktwo.rot = [0, 0, float(radians(theta1))]##### rotating link two around its pivot point using euler angles
               theta1=theta1+theta1_inc             
               linkthree.rot =[ 0, float(radians(theta2)), 0]
               theta2=theta2+theta2_inc                
               linkfour.rot = [0, float(radians(theta3)), 0]
               theta3=theta3+theta3_inc
               linkfive.rot = [float(radians(theta4)), 0, 0]
               theta4=theta4+theta4_inc
               linksix.rot = [0, float(radians(theta5)), 0]
               theta5=theta5+theta5_inc
               tool.rot = [float(radians(theta6)), 0, 0]
               theta6=theta6+theta6_inc 
               toolpiston.rot = [0, 0, 0] ###### there is not rotation here but it is required to update the object 
               Redraw()
