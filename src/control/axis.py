"""
Fields to be included in the control table:
- dm
- Norte (Proyecto)
- Este  (Proyecto)
- Norte (Control)
- Este  (Control)
- Diferencia
- Cumple
"""




import numpy as np
import utils
import sys
from control.range import ControlRangeList

TOLERANCE = 0.10

class Axis :
    """represents the 'eje-estaca' file"""
    def __init__ (self, filename) :
        self.filename  = filename
        self.matrix    = utils.read_csv(filename, cols=(0,1,2))
        # self.dm_coor   = {row[0]: (utils.str_to_flt(row[1]),utils.str_to_flt(row[2])) for row in self.matrix}
        self.dm_coor   = {row[0]: (row[1],row[2]) for row in self.matrix}
 
    def get_dm_list (self):
        return self.matrix[:,0]
    
    def get_coor (self, dm) :
        return self.dm_coor.get(dm)




class AxisControlPoint :
    
    def __init__ (self, dm, x_proj, y_proj, x_ctrl, y_ctrl, distance, good) :
        
        self.dm = dm
        
        self.x_proj = x_proj
        self.y_proj = y_proj
        
        self.x_ctrl = x_ctrl
        self.y_ctrl = y_ctrl
        
        self.distance = distance
        
        self.good = good
    
    def __str__ (self) :
        return f'dm={self.dm}'
    
    def __lt__ (self, point) :
        return float(self.dm) < float(point.dm)
    
    def __le__ (self, point) :
        return float(self.dm) <= float(point.dm)



class AxisControl :
    
    def __init__ (self, filename_proj, filename_ctrl) :
        # Axis file models for project and control
        self.axis_proj = Axis(filename_proj)
        self.axis_ctrl = Axis(filename_ctrl)
        
        
        
        # Project and Control dm lists
        self.project_dm_list = self.axis_proj.get_dm_list()
        self.control_dm_list = self.axis_ctrl.get_dm_list()
        self.dm_list         = sorted(
            np.intersect1d(self.project_dm_list,self.control_dm_list),
            key = float
        )
        self.tolerance       = 0.10
        
        min_proj_dm = utils.str_to_flt(min(self.project_dm_list,key=float))
        max_proj_dm = utils.str_to_flt(max(self.project_dm_list,key=float))
        self.total_length = np.round(max_proj_dm-min_proj_dm,3)
        
        self.min_ctrl_dm = utils.str_to_flt(min(self.dm_list, key=float))
        self.max_ctrl_dm = utils.str_to_flt(max(self.dm_list, key=float))
        
        self.ctrl_length = np.round(self.max_ctrl_dm - self.min_ctrl_dm,3)
        
        
        self.point_list = []
        self.control()
        self.point_list.sort()
    
 
    def control (self,output_filename="") :
        output = np.empty((0,7))
        for dm in self.dm_list:
            
            xp , yp  = self.axis_proj.get_coor(dm)
            xc , yc  = self.axis_ctrl.get_coor(dm)
            delta    = utils.euc_dist(
                utils.str_to_flt (xp),
                utils.str_to_flt (yp),
                utils.str_to_flt (xc),
                utils.str_to_flt (yc),
            )
            
            row = np.array([
                dm,
                xp,
                yp,
                xc,
                yc,
                utils.format_float(delta),
                "SI" if delta <= TOLERANCE else "NO"
            ])
            
            output = np.vstack((output, row))
            
            point = AxisControlPoint(
                dm, xp, yp, xc, yc,
                utils.format_float(delta),
                'SI' if delta <= TOLERANCE else 'NO'
            )
            
            self.point_list.append(point)
        
        # utils.write_csv(output_filename, output)
        # return output
    
    def write (self,output_filename='') :
        output_matrix = np.empty((0,7))
        for point in self.point_list:
            row = np.array([
                point.dm,
                point.x_proj,
                point.y_proj,
                point.x_ctrl,
                point.y_ctrl,
                point.distance,
                point.good,
            ])
            output_matrix = np.vstack ((output_matrix, row))
            
        utils.write_csv(output_filename, output_matrix)





def main (input1, input2, output) :
    
    file_proj = input1
    file_ctrl = input2
    
    level_control = AxisControl(file_proj,file_ctrl)
    level_control.write(output)

if __name__ == '__main__':
    
    main(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3]
    )
