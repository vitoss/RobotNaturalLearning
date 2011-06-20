#Loading and intepreting file
#Author: Witold Wasilewski 2011

import os.path
from LineInterpreter import LineInterpreter

class SequenceFileManager:
	
	def load( self, sequence, filename ):
		if os.path.exists(filename):
			#reading from file
			file = open(filename, "r")
			interpreter = LineInterpreter()
			
			for line in file:
				if len(line) > 0:
					interpreter.interpret( sequence, line )
				
			file.close()
		else:
			raise Exception("Filename not found")
		
		
	def save( self, sequence, filename ):
		file = open(filename, "w")
		#
		
		#
		file.close()