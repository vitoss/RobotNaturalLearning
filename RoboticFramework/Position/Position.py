#Abstract position class
# Author: Witold Wasilewski 2011

class Position:
	_value = 0
	type = "Abstract"
	
	def __init__(self, value):
		self._value = list(value)
	
	def getValue(self):
		return self._value