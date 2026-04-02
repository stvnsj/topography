import numpy as np
import sys
import utils

class Reader :
    
    def __init__(self,path1,path2,path3):
        
        if path1:
            self.matrix = np.round(np.genfromtxt(path1, delimiter=',', skip_header=0,invalid_raise=False),3)
            self.labels = np.genfromtxt(path1, delimiter=',', dtype=str, skip_header=0,invalid_raise=False)[:,4]
        else:
            self.matrix = None
            self.labels = None
            
        if path2:
            self.oriented_matrix = np.round(np.genfromtxt(path2, delimiter=',', skip_header=0,invalid_raise=False),3)
            self.oriented_labels = np.genfromtxt(path2, delimiter=',', dtype=str, skip_header=0,invalid_raise=False)[:,4]
            
        else:
            self.oriented_matrix = None
            self.oriented_labels = None
            
        if path3 : 
            self.heights = utils.normalize_fstring_array(np.genfromtxt(path3, delimiter=',', skip_header=0, dtype=str,invalid_raise=False))
            
        else :
            self.heights = None
    
    
    def getData (self) :
        return self.matrix, self.labels, self.oriented_matrix, self.oriented_labels, self.heights




