"""
Los campos del control de línea de tierra transversal son:
- dm               DONE   0
- lado             DONE   1
- distancia        DONE   2
- cota control     DONE   3
- cota estudio     DONE   4
- tipo terreno     DONE   5
- tolerancia       DONE   6
- diferencia       DONE   7
- cumple           DONE   8
"""

import numpy as np
import utils
import bisect
import re
import sys
from control.range import ControlRangeList

# 42  ---> demás ejes
# 108 ---> 70.0% # Eje 27

tolerance = {
    0  : 0.00,
    1  : 0.02,
    2  : 0.05,
    3  : 0.10,
    4  : 0.25,
}

class Line :
    
    def __init__(self,point1,point2):
        # PUNTOS DE PROYECTO
        self.x0 = point1.distance
        self.y0 = point1.height
        
        self.x1 = point2.distance
        self.y1 = point2.height
        # PENDIENTE DE LA RECTA
        self.slope = (self.y1-self.y0) / (self.x1-self.x0)
    
    def get_y (self,x) :
        y = np.round(self.slope * (x - self.x0) + self.y0, 3) # Redondeado
        #y = self.slope * (x - self.x0) + self.y0 # Sin redondear
        return y
    
    def contains_x (self,x) :
        return (self.x0 <= x and x <= self.x1)
    
    def __str__ (self):
        return f'x0={self.x0}  \t x1={self.x1}\ny0={self.y0}  \ty1={self.y1}'


class RandomMatrixIterator :
    
    def __init__ (self,matrix):
        self.matrix    = matrix
        self.index     = 0
        self.length    = len(matrix)
    
    def __iter__ (self):
        return self
    
    def __next__ (self):
        
        
        if self.index >= self.length :
            raise StopIteration
        
        START = 0
        END   = 0
        
        for i in range(self.index, self.length):
            
            if i == self.length-1:
                START = self.index
                END = i
                self.index = i + 1
                return self.matrix[START:END+1]
            
            if self.matrix[i][0] != self.matrix[i+1][0]:
                START = self.index
                END   = i
                self.index = i + 1
                return self.matrix[START : END+1]


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

class MOPPoint :
    
    def __init__ (self, distance, height, descr, axis = False):
        self.distance   = utils.str_to_flt (distance)
        self.height     = utils.str_to_flt (height)
        self.descriptor = descr
        self.axis       = axis
    
    def get_ground_type(self):
        match = re.search(r'\d+', self.descriptor)
        if match:
            
            return int(match.group())
        print(self.descriptor)
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
        

class MOPSection:
    
    def __init__ (self, matrix):
        
        self.dm = matrix[0][0]
        
        self.point_list = []
        
        for row in matrix :
            try:
                point = MOPPoint(row[1],row[2],row[3], axis = True if float(row[1]) == 0 else False)
                self.point_list.append(point)
            except:
                print("ERRORR BUILDING MOP POINT " , row)
                pass
        
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
        return ''



class MOPControlPoint :
    
    def __init__ (
            self,
            dist,
            proj_height,
            ctrl_height,
            descr,
            delta_y,
            dm = "",
    ):
        
        self.distance         = dist
        self.proj_height      = proj_height 
        self.ctrl_height      = ctrl_height
        self.descriptor       = descr
        self.delta            = delta_y
        self.tolerance_weight = 10 if self.is_within_tolerance() else 0
        
        if delta_y is None:
            self.weight = 0
        elif np.abs(dist) < 0.001:
            self.weight = 0
        elif np.abs(dist) < 6.000:
            self.weight = 10 + self.tolerance_weight
        elif np.abs(dist) < 9.000:
            self.weight = 7  + self.tolerance_weight
        elif np.abs(dist) < 12.000:
            self.weight = 4  + self.tolerance_weight
        else:
            self.weight = 2  + self.tolerance_weight
    
    def __lt__ (self, point):
        return self.distance <  point.distance
    def __le__ (self, point):
        return self.distance <= point.distance
    def __str__ (self) :
        return f'Point: dist={self.distance} ; cota = {self.ctrl_height}'
    
    def get_ground_type(self):
        # Use regular expression to find the number in the string
        match = re.search(r'\d+', self.descriptor)
        if match:
            return int(match.group())
        return 0
    
    def get_tolerance (self) :
        return tolerance.get(self.get_ground_type(), 0.000)
    
    def is_within_tolerance (self) :
        ground_type = self.get_ground_type()
        tol = tolerance[ground_type]
        try:
            if np.abs(self.delta) > tol:
                return False
            return True
        except:
            return False
    
    def get_side (self) :
        if self.distance < 0 :
            return "i"
        elif self.distance > 0 :
            return "d"
        else :
            return "c"



class MOPControlSection :
    
    def __init__ (self, dm, point_list, optimize=False):
        self.dm         = dm
        self.point_list = point_list
        self.optimize   = optimize
    
    def select_random_points (self):
        zero_point = MOPControlPoint(0,0,0,'',0)
        index = bisect.bisect_left (self.point_list, zero_point)
        
        neg_distr = np.array([p.weight for p in self.point_list[0:index]])
        pos_distr = np.array([p.weight for p in self.point_list[index+1:]])
        
        pointsA = np.array([])
        pointsB = np.array([])
        
        for i in range(0,4):
            SAMPLE_SIZE = 3 - i
            try:
                pointsA = np.random.choice(self.point_list[0:index], size=SAMPLE_SIZE, replace=False, p=neg_distr/sum(neg_distr))
                break
            except:
                if SAMPLE_SIZE > 1:
                    continue
                else:
                    if not self.optimize:
                        print(f'No se seleccionaron puntos negativos para dm = {self.dm}')
                    pointsA = np.array([])
                    break
        
        for i in range(0,4):
            SAMPLE_SIZE = 3-i
            try:
                pointsB = np.random.choice(self.point_list[index+1:], size=SAMPLE_SIZE, replace=False, p=pos_distr/sum(pos_distr))
                break
            except:
                if SAMPLE_SIZE > 1:
                    continue
                else:
                    if not self.optimize:
                        print(f'No se seleccionaron puntos positivos para dm = {self.dm}')
                    pointsB = np.array([])
                    break
        
        random_points = np.sort(np.concatenate(( pointsA , pointsB )))
        #for p in random_points:
        #    print(p)
        #print(random_points)
        return random_points

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
    

class MOPControl :
    
    def __init__ (self, filename_proj, filename_ctrl, optimize = False):
        
        self.optimize = optimize
        self.mop_proj = MOP(filename_proj)
        self.mop_ctrl = MOP(filename_ctrl)
        
        self.project_dm_list = self.mop_proj.get_dm_list()
        self.control_dm_list = self.mop_ctrl.get_dm_list()
        self.dm_list         = sorted(
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
        
        # List of control sections.
        self.control_section_list = []
        self.TOTAL                = 0
        
        # Matrix for the CSV control file. (Not Random)
        self.control_matrix       = np.empty((0,9))
        self.__control__()
        #self.print_control_stats()
    
    
    def __control__ (self) :
        # iterate over project dm's 
        for dm in self.dm_list:
            
            proj_section = self.mop_proj.get_section(dm)
            ctrl_section = self.mop_ctrl.get_section(dm)
            proj_height  = 0
            mop_control_point_list = []            
            
            for point_ctrl in ctrl_section.point_list:
                
                pair = proj_section.get_neighbor_indices(point_ctrl)
                
                if pair is not None and not point_ctrl.axis:
                    
                    point_proj_1 = proj_section.get_point(pair[0])
                    point_proj_2 = proj_section.get_point(pair[1])
                    line = Line(point_proj_1,point_proj_2)
                    y = line.get_y(point_ctrl.distance)
                    DELTA = np.round(np.abs(y-point_ctrl.height),3)
                    proj_height = y
                    
                    new_row = np.array([
                        dm,
                        "i" if point_ctrl.distance < 0 else "d",
                        utils.format_float(point_ctrl.distance),
                        utils.format_float(point_ctrl.height),
                        utils.format_float(y),
                        str(point_ctrl.get_ground_type()),
                        utils.format_float(tolerance.get(point_ctrl.get_ground_type(),0.000)),
                        utils.format_float(np.abs(DELTA)),
                        "Cumple" if point_ctrl.in_tolerance(DELTA) else "No cumple"
                    ])
                    
                    self.control_matrix = np.vstack((self.control_matrix,new_row))
                    
                    mop_control_point = MOPControlPoint(
                        point_ctrl.distance,
                        proj_height,
                        point_ctrl.height,
                        point_ctrl.descriptor,
                        DELTA
                    )
                    
                    mop_control_point_list.append(mop_control_point)
            
            self.control_section_list.append(MOPControlSection(dm,mop_control_point_list, optimize=self.optimize))
 
 
    def write(self, outputfile=""):
        header = "DM,lado,distancia,cota ctrl,cota topo,tipo,tolerancia,delta,cumple"
        utils.write_csv(outputfile, self.control_matrix, header=header)
    
    
    
    def eval_seed(self, seed=42):
        
        np.random.seed(seed)
        TOTAL_POINTS = 0
        OK_POINTS    = 0
        for sec in self.control_section_list:
            rand_points = sec.select_random_points()
            for p in rand_points:
                TOTAL_POINTS += 1
                OK_POINTS    = OK_POINTS + (1 if p.is_within_tolerance() else 0)
        
     
        PERCENT = np.round(100 * OK_POINTS / TOTAL_POINTS, 1)
        return PERCENT
    
    
    def optimize_seed (self, seed=42, tries=1000):
        OPTIMAL_SEED=seed
        OPTIMAL_PERCENT=0.0
        for i in range(seed,seed+tries):
            CURR_PERCENT = self.eval_seed(seed = i)
            if OPTIMAL_PERCENT <= CURR_PERCENT:
                OPTIMAL_SEED = i
                OPTIMAL_PERCENT = CURR_PERCENT
        
        print(f'Rango de Búsqueda de Semilla : {seed} ; {seed + tries}')
        print(f'Semilla Óptima               : {OPTIMAL_SEED}')
        print(f'Porcentaje Máximo            : {OPTIMAL_PERCENT}')
    
    
    def select_random_points(self, seed=42):
        
        np.random.seed(seed)
        random_table = np.empty((0,9))
        TOTAL_POINTS = 0
        OK_POINTS    = 0
        for sec in self.control_section_list:
            
            rand_points = sec.select_random_points()
            
            for p in rand_points:
                
                row = np.array([
                    sec.dm,
                    p.get_side(),
                    p.distance,
                    p.ctrl_height,
                    p.proj_height,
                    p.get_ground_type(),
                    p.get_tolerance(),
                    p.delta,
                    p.is_within_tolerance()
                ])
                
                TOTAL_POINTS += 1
                OK_POINTS    = OK_POINTS + (1 if p.is_within_tolerance() else 0)
                random_table = np.vstack((random_table,row))
        
        PERCENT = np.round(100 * OK_POINTS / TOTAL_POINTS, 1)
        # print(f"Porcentaje de Puntos dentro de Tolerancia: {PERCENT}%")
        # utils.write_csv(outputfile, random_table)
        return RandomMop(random_table,self.min_ctrl_dm,self.max_ctrl_dm,self.proj_length,TOTAL_POINTS,OK_POINTS, PERCENT)


"""
This class models the random selection of
points from the control of mop.
It includes:
 - Length of project axis
 - Length of control axis
 - Percentage of controlled length 
 - Percentage of points within tolerance
"""
class RandomMop :
    
    def __init__(self, matrix, min_ctrl_dm, max_ctrl_dm, proj_length, ctrl_number, good_number, good_percent) :
        
        
        self.section_list = []
        self.min_ctrl_dm  = min_ctrl_dm
        self.max_ctrl_dm  = max_ctrl_dm
        self.proj_length  = proj_length
        self.ctrl_number  = ctrl_number
        self.good_number  = good_number
        self.good_percent = good_percent
        
        for mat in RandomMatrixIterator(matrix):
            m = RandomMopSection(mat)
            self.section_list.append(m)
        self.section_list.sort()
        
    def coverage_percent (self):
        COVERAGE = np.round(self.max_ctrl_dm - self.min_ctrl_dm,3)
        PERCENT = (100 * COVERAGE) / self.proj_length
        return np.round(PERCENT,3)
    
    def section_number (self) :
        return len(self.section_list)
    
    def ctrl_length (self) :
        return np.round(self.max_ctrl_dm - self.min_ctrl_dm,3)
    
    def sections_per_km (self) :
        np.round(1000 * self.ctrl_number / self.proj_length)
        
    def required_sections_per_km (self) :
        return np.ceil(25 * self.proj_length / 1000)
    
    def sufficient_points (self) :
        return self.section_number() >= self.required_sections_per_km()
    
    
    def write(self, output_filename) :
        
        output_matrix = np.empty((0,8))
        
        for sec in self.section_list:
            
            for point in sec.pos_points:
                row = np.array([
                    sec.dm,
                    point.distance,
                    point.ctrl_height,
                    point.proj_height,
                    point.type,
                    point.tol,
                    point.dif,
                    point.good
                ])
                
                output_matrix = np.vstack((output_matrix, row))
                
            for point in sec.neg_points:
                
                row = np.array([
                    sec.dm,
                    point.distance,
                    point.ctrl_height,
                    point.proj_height,
                    point.type,
                    point.tol,
                    point.dif,
                    point.good
                ])
                
                output_matrix = np.vstack((output_matrix, row))
        
        print("Porcentaje: " , self.good_percent)
        header = "DM,distancia,cota ctrl,cota topo,tipo,tolerancia,delta,cumple"
        utils.write_csv(output_filename, output_matrix,header=header)



class RandomMopSection :
    
    def __init__ (self, matrix) :
        self.dm = matrix[0][0]
        self.pos_points = []
        self.neg_points = []
        
        for row in matrix:
            point = RandomMopPoint (
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
            )
            if float(row[2]) > 0 :
                self.pos_points.append(point)
            else:
                self.neg_points.append(point)
    
    
    def __lt__ (self, section) :
        return float(self.dm) < float(section.dm)
    def __le__ (self, section) :
        return float(self.dm) <= float(section.dm)
    def __str__ (self, section) :
        return f'Random MOP Section {self.dm}'


class RandomMopPoint :
    
    def __init__ (self, distance, ctrl_height, proj_height, tipo, tol, dif, good) :
        self.distance     = distance
        self.ctrl_height  = ctrl_height
        self.proj_height  = proj_height
        self.type         = tipo
        self.tol          = tol
        self.dif          = dif
        self.good         = good
        
    
    def __str__ (self):
        return f'point\ndist={self.distance}\nctrl={self.ctrl_height}\nproj={self.proj_height}\nTip={self.type}\nTOL={self.tol}\ndif={self.dif}\nok={self.good}\n'


def main (input1,input2,output) :    
    mop_control = MOPControl( input1, input2 )
    mop_control.write(output)
    mop_random_control = mop_control.select_random_points().write(output)

if __name__ == '__main__':
    main(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3]
    )
