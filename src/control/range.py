import numpy as np
import utils


# Each type of control should report:
# - Number of controled points
# - Percentage of control coverage
# - Percentage of verified points (from the total)



#---------------------------------------------
#  DM0  |  DM1  | NAME |
#---------------------------------------------


class ControlRangeList:
    
    def __init__ (self, filename):    
        matrix = utils.read_csv(filename)
        #print(matrix)
        self.control_range_list = []
        self.__init_control_range_list__(matrix)  
 
    def __init_control_range_list__ (self, matrix):
        if matrix.ndim == 1:
            control_range = ControlRange(matrix[0], matrix[1], matrix[2])
            self.control_range_list.append(control_range)
            return
        for row in matrix:
            control_range = ControlRange(row[0],row[1],row[2])
            self.control_range_list.append(control_range)
 
    def filter_dm_list(self, dm_list):
        """Takes a list of dm's and returns the sublist of all dm's
        which are to be controlled."""
        control_dm_list = []
        for control_range in self.control_range_list:
            control_dm_list = control_dm_list + control_range.filter_dm_list(dm_list)        
        return control_dm_list
    
    def get_range_name(self, dm) :
        for ran in self.control_range_list:
            if ran.contains(dm):
                return ran.name
        return None
    
    def __str__ (self):
        string = ''
        for x in self.control_range_list:
            print(x)
        return ''


class ControlRange:
    
    def __init__ (self, dm0, dm1, name):
        print(dm0)
        print(dm1)
        print(name)
        self.dm0    = np.round(float(dm0),3)
        self.dm1    = np.round(float(dm1),3)
        self.name   = name
        self.length = self.dm1 - self.dm0
    
    def get_start_point(self):
        """Returns the first point in the control range"""
        return self.dm0
    
    def get_end_point(self):
        """Returns the final point in the control range"""
        return self.dm1
    
    def contains(self,dm):
        """Returns True if this control range contains the argument dm"""
        return (self.dm0 <= np.round(float(dm),3) and np.round(float(dm),3) <= self.dm1)
    
    def filter_dm_list (self, dm_list) :
        """Takes a list of dm's and returns the sublist of all dm's
        which are part of this control range"""
        control_dm_list = []
        for dm in dm_list:
            if self.contains(dm):
                control_dm_list.append(dm)
        return control_dm_list
    
    def __str__ (self) :
        return f'start = {self.dm0}\nend = {self.dm1}\nname = {self.name}\nlength = {self.length}\n--------------------------'







def main () :
    
    control_range_list = ControlRangeList('/home/jstvns/axis/eqc-input/control-level/tramos.csv')
    
    mat = utils.read_csv('/home/jstvns/axis/eqc-input/control-level/longi-ctrl-complete.csv')
    
    dm_list = mat[:,0]
    
    print(control_range_list)
    print(control_range_list.filter_dm_list(dm_list))

if __name__ == '__main__' :
    main () 
