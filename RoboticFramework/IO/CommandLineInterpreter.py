#Intepreting Commands
#Author: Witold Wasilewski 2011

import RoboticFramework.Command.CommandList as CommandList
import RoboticFramework.Command.CommandLoop as CommandLoop
import PositionCommandLineInterpreter
import RoboticFramework.Command.MoveToPositionCommand as MoveToPositionCommand

class CommandLineInterpreter:
    
    def __init__(self):
        rootCommandList = CommandList.CommandList()
        self.stack = []
        self.stack.append(rootCommandList)
        self.currentList = rootCommandList
        self.lineInterpreter = PositionCommandLineInterpreter.PositionCommandLineInterpreter()
    
    def __init__(self, rootCommandList):
        self.stack = []
        self.stack.append(rootCommandList)
        self.currentList = rootCommandList
        self.lineInterpreter = PositionCommandLineInterpreter.PositionCommandLineInterpreter()
        
    def interpret( self, line ):
        #all the magic here
        line = line.strip()
        
         #if comments -> continue
        if line[0] == '#':
            return -1
            
        newPosition = -1
        splitedLine = line.split('(')
        functionName = splitedLine[0].strip()
        
        #checking if we've got input arguments at all
        if len(splitedLine) > 1:
            inputsString = splitedLine[1].strip().replace(")","").strip()
        
        if functionName == "loop":
            newLoop = CommandLoop.CommandLoop()
            newList = CommandList.CommandList()
            newLoop.command = newList
            newLoop.counter = float(inputsString)
            self.currentList.add(newLoop)
            self.currentList = newList
            self.stack.append(list)
        elif functionName == "endloop":
            self.stack.pop() #removing currentlist from stack
            
            #currentList to previous list
            previousList = self.stack.pop()
            self.stack.append(previousList)
            self.currentList = previousList
        else:
            #interpret line as new position
            newPositionCommand = self.lineInterpreter.interpretLine(line)
            self.currentList.add(newPositionCommand)
            
        
