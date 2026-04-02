
"""

"""

import numpy as np
import utils
import bisect
import re
import sys
from control.range import ControlRangeList

# 42  ---> demás ejes
# 108 ---> 70.0% # Eje 27


TOLERANCE = 0.500


class MopMatrixIterator :
    
    def __init__ (self, matrix) :
        self.matrix = matrix
        self.index  = 1
        self.length = len(matrix)
        
    
    def __iter__ (self) :
        return self
    
    def __next__ (self) :
        
        if self.index >= self.length :
            raise StopIteration
        
        START = 0
        END   = 0
        
        for i in range(self.index, self.length):
            # This is the first index of the following section
            if self.matrix[i][0] != '' or i == self.length - 1:
                START      = self.index - 1
                END        = i
                self.index = i + 1
                break
        
        return self.matrix[START:END]   



class MOP :
    
    def __init__ (self, filename) :
        
        self.filename = filename
        self.matrix = utils.read_csv(filename)
        self.section_list = []
        self.dm_list = []
        self.dm_section = {}
        
        
        i = 0
        for sec in MopMatrixIterator(self.matrix):
            section = MOPSection(sec)
            self.dm_section[section.dm] = i
            self.dm_list.append(section.dm)
            self.section_list.append(section)
            i += 1
        self.size = len(self.section_list)
    
    
    def get_dm_list (self) :
        return self.dm_list
    
    def get_section (self,dm) :
        idx = self.dm_section.get(dm, None)
        if idx is None:
            return None
        return self.section_list[self.dm_section[dm]]


class MOPSection:
    
    def __init__ (self, matrix):
        
        self.dm = matrix[0][0]
        self.point_list = []
        self.dist_point = {}
        
        for row in matrix :
            point = MOPPoint(row[1],row[2],row[3])
            self.dist_point[row[1]] = point
            self.point_list.append(point)
        self.size = len(matrix)
        self.point_list.sort()
        
        self.__min_dist__   = min(self.point_list)
        self.__max_dist__   = max(self.point_list)
        self.__min_height__ = min(self.point_list, key=lambda point: point.height)
        self.__max_height__ = max(self.point_list, key=lambda point: point.height)
        
    def get_size(self):
        return self.size
    
    def get_min_dist (self):
        return self.__min_dist__

    def get_max_dist (self):
        return self.__max_dist__
    
    def get_min_height (self):
        return self.__min_height__
    
    def get_max_height (self):
        return self.__max_height__
    
    def get_bisection_index (self, point):
        return bisect.bisect_left(self.point_list, point)
    
    def get_neighbor_indices(self, point):
        i0 = self.get_bisection_index(point)
        if i0 == 0 or i0 == self.size:
            return None
        return (i0-1,i0)

    def get_point(self, index):
        return self.point_list[index]
    
    def __str__(self):
        #for p in self.point_list:
        #    print(p)
        return f'MOP Section {self.dm}'

class MOPPoint :
    
    def __init__ (self, distance, height, descr):
        self.distance   = utils.str_to_flt (distance)
        self.height     = utils.str_to_flt (height)
        self.descriptor = descr
    
    def get_ground_type(self):
        match = re.search(r'\d+', self.descriptor)
        if match:
            return int(match.group())
        return 0
    
    def in_tolerance (self, delta):
        tol = tolerance.get(self.get_ground_type(), 0.000)
        if np.abs(delta) > tol :
            return False
        return True
    
    def __lt__ (self,point):
        return self.distance <  point.distance
    def __le__ (self,point):
        return self.distance <= point.distance
    def __str__(self):
        return f'd={self.distance}; h={self.height}, dscr={self.descriptor}'



class MDTControl :
    
    
    def __init__ (self, filename_proj, filename_ctrl):
        
        self.mop_proj = MOP(filename_proj)
        self.mop_ctrl = MOP(filename_ctrl)
        
        self.project_dm_list = self.mop_proj.get_dm_list()
        self.control_dm_list = self.mop_ctrl.get_dm_list()
        
        self.dm_list        = sorted(
            np.intersect1d(self.project_dm_list,self.control_dm_list),
            key = float
        )
        
        self.min_ctrl_dm   = np.round(np.min(np.array(self.dm_list).astype(float)),3)
        self.max_ctrl_dm   = np.round(np.max(np.array(self.dm_list).astype(float)),3)
        self.ctrl_length   = self.max_ctrl_dm - self.min_ctrl_dm
        
        min_proj_dm   = np.round(np.min(np.array(self.project_dm_list).astype(float)),3)
        max_proj_dm   = np.round(np.max(np.array(self.project_dm_list).astype(float)),3)
        self.proj_length = max_proj_dm - min_proj_dm
        
        self.ctrl_dm_number = len(self.dm_list)
        
        self.control_section_list = []
        self.TOTAL_POINTS         = 0
        self.GOOD_POINTS          = 0
        self.control_matrix       = np.empty((0,9))
        
        self.section_list = []
        self.__control__()
        self.section_list.sort()
        
    
    
    def __control__ (self) :
        # iterate over project dm's 
        for dm in self.dm_list:
            point_list = []
            sec_proj = self.mop_proj.get_section(dm)
            sec_ctrl = self.mop_ctrl.get_section(dm)
            for dist in sec_proj.dist_point:
                ctrl_point = sec_proj.dist_point.get(dist)
                proj_point = sec_ctrl.dist_point.get(dist)
                mdt_point = MDTControlPoint(dist, proj_point.height, ctrl_point.height)
                if mdt_point.is_within_tolerance():
                    self.GOOD_POINTS += 1
                self.TOTAL_POINTS += 1
                point_list.append(mdt_point)
            mdt_section = MDTControlSection(dm,point_list)
            self.section_list.append(mdt_section)
    
    def point_length (self) :
        LENGTH = 0
        for sec in self.section_list :
            LENGTH += sec.point_length()
        return LENGTH
    
    def section_length (self) :
        return len(self.section_list)
    
    def get_total_points (self) :
        return self.TOTAL_POINTS
    
    def get_good_points (self) :
        return self.GOOD_POINTS
    
    def get_good_percent (self) :
        PERCENT = np.round(100 * self.get_good_points() / self.get_total_points(), 1)
        return PERCENT
    
    def write( self, output_filename):
        output_matrix = np.empty((0,6))
        for sec in self.section_list:
            for point in sec.point_list:
                row = np.array([
                    sec.dm,
                    point.distance,
                    point.ctrl_height,
                    point.proj_height,
                    utils.format_float(point.abs_delta),
                    str(point.is_within_tolerance()),
                ])
        utils.write_csv(output_filename,output_matrix)


class MDTControlSection :
    
    def __init__ (self, dm, point_list):
        self.dm         = dm
        self.point_list = point_list
    
    
    def point_length (self) :
        return len(self.point_list)
    
    def __lt__ (self, point) :
        return float(self.dm) < float(point.dm)
    
    def __le__ (self, point) :
        return float(self.dm) <= float(point.dm)
    
    def __str__ (self):
        return f'MDT Section dm = {self.dm}'
    
    def point_length (self) :
        return len(self.point_list)


"""
According to the ANNEX,
This point is to contain the
following fields:
- Side
- Distance
- Ctrl Height
- Proj Height
- Delta
- Absolute Delta
- Cumple
"""
class MDTControlPoint :
    
    def __init__ (
            self,
            dist,
            proj_height,
            ctrl_height,
            dm = "",
    ):
        
        self.distance         = dist
        self.proj_height      = proj_height 
        self.ctrl_height      = ctrl_height
    
    def __lt__ (self, point):
        return self.distance <  point.distance
    def __le__ (self, point):
        return self.distance <= point.distance
    def __str__ (self) :
        return f'Point: dist={self.distance} ; cota = {self.ctrl_height}'
    
    def delta (self) :
        ctrl_z = utils.str_to_flt(self.ctrl_height)
        proj_z = utils.str_to_flt(self.proj_height)
        return np.round(ctrl_z - proj_z, 3)
    
    def abs_delta (self) :
        return np.abs(self.delta())
    
    def is_within_tolerance (self) :
        return self.delta() <= TOLERANCE
    
    def get_side (self) :
        if self.distance == "0.000":
            return "E"
        if float(self.distance) < 0 :
            return "I"
        if float(self.distance) > 0 :
            return "D"
        return "null"
    
    def __str__ (self) :
        return f'd={self.distance};hc={self.ctrl_height};hp={self.proj_height}'


def main (input1,input2,output) :
    mop_control = MDTControl( input1, input2 )
    mop_control.write(output)
    return


if __name__ == '__main__':
    main(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
    )
