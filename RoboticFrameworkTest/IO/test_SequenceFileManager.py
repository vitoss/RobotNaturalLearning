#Testing sequence file manager
#Author: Witold Wasilewski

from RoboticFramework.IO.SequenceFileManager import SequenceFileManager
from RoboticFramework.Position.PositionSequence import PositionSequence
from RoboticFramework.Position.JointPosition import JointPosition
import os.path
import py.test

class TestSequenceFileManager:
    
    def setup_method(self, method):
        self.manager = SequenceFileManager()
        self.sequence = PositionSequence([])
        
    def test_load_simpleJointFile(self):
        self.manager.load(self.sequence, "data/simple.txt")
        
        assert self.sequence.amount() == 3
    
    def test_save_simpleJointFile_fileCreation(self):
        preparedSequence = self.preparePositionSequence()
        targetFilepath = "data/temp.txt"
        self.manager.save(preparedSequence, targetFilepath)
        
        assert os.path.exists(targetFilepath) 
        os.remove(targetFilepath)
        
    def test_save_simpleJointFile_simple(self):
        preparedSequence = self.preparePositionSequence()
        targetFilepath = "data/temp.txt"
        self.manager.save(preparedSequence, targetFilepath)
        
        #load and test
        loadedSequence = PositionSequence([])
        self.manager.load(loadedSequence, targetFilepath)
        
        assert loadedSequence.amount() == 100, "Sequence should consist of 100 positions"
        
        os.remove(targetFilepath)
        
    
    def test_load_fileNotFound(self):
        try:
            self.manager.load(self.sequence, "dummyFileDoesnExists.txt")
        except:
            assert py.test.raises(Exception, "Filename not found")
            return
        
        assert False, "Exception not thrown"
    
    #helpers
    def preparePositionSequence(self):
        sequence = PositionSequence([])
        for i in range(0,100):
            sequence.appendPosition(JointPosition([0*i,1*i,2*i,3*i,4*i,5*i]))
        
        return sequence
    
    def teardown_method(self, method):
        self.manager = 0
        self.sequence = 0