"""
The control of levels should consider the following fields:
- DM
- Ctrl Height
- Proj Height
- Delta
- Cumple
"""

import numpy as np
import utils


class Longitudinal:
    """Represents the longitudinal file || dm | cota || """
    def __init__ (self, filename):
        self.filename = filename
        self.matrix = utils.read_csv(filename)
        self.dm_height = dict(self.matrix)
        
    def get_height(self, dm):
        """Returns the height associated with some dm"""
        try:
            return self.dm_height[dm]
        except:
            print(f'No se encuentra el dm {dm} en el archivo {self.filename}')
    
    def get_dm_list (self) :
        return self.matrix[:,0]
    
    def get_height_list (self) :
        return self.matrix[:,1]


class LevelControl:
    """It compares the project and control longitudinal files"""
    
    def __init__ (self,filename_proj, filename_ctrl):
        
        #longitudinal file models for project and control
        self.longitudinal_proj = Longitudinal(filename_proj)
        self.longitudinal_ctrl = Longitudinal(filename_ctrl)
        
        
        # Project and Control dm lists
        self.project_dm_list = self.longitudinal_proj.get_dm_list()
        self.control_dm_list = self.longitudinal_ctrl.get_dm_list()
        self.dm_list         = sorted(
            np.intersect1d(self.project_dm_list,self.control_dm_list),
            key=float
            
        )
        self.point_list      = []
        self.__control__()
        
        self.point_list.sort()
        
        

    def __control__ (self) :
        
        for dm in self.dm_list:
            proj_height = utils.str_to_flt( self.longitudinal_proj.get_height(dm))
            ctrl_height = utils.str_to_flt( self.longitudinal_ctrl.get_height(dm))
            delta = np.round(np.abs(proj_height - ctrl_height), 3)
            good = "SI" if delta <= 0.01 else 'NO'
            row = np.array([dm,ctrl_height,proj_height,delta,good])
            point = LevelControlPoint(
                dm,
                self.longitudinal_proj.get_height(dm),
                self.longitudinal_ctrl.get_height(dm),
                utils.format_float(delta),
                good
            )
            self.point_list.append(point)
 
    def write (self , output_filename) :
        output_matrix = np.empty((0,5))
        for point in self.point_list :
            row = np.array([point.dm,point.proj_height,point.ctrl_height,point.delta, point.good])
            output_matrix = np.vstack((output_matrix, row))
        utils.write_csv(output_filename, output_matrix)


class LevelControlPoint :
    def __init__ (self, dm, proj_height, ctrl_height, delta, good):
        self.dm = dm
        self.proj_height = proj_height
        self.ctrl_height = ctrl_height
        self.delta = delta
        self.good  = good
        
    
    def __lt__ (self, point) :
        return float(self.dm) < float(point.dm)
    
    
    def __le__ (self, point) :
        return float(self.dm) <= float(point.dm)
    
    def __eq__ (self, point) :
        return self.dm == point.dm

    def __str__ (self) :
        return f'dm = {self.dm}'


def main () :
    
    file_proj = '/home/jstvns/axis/eqc-input/control-level/longi-proj.csv'
    file_ctrl = '/home/jstvns/axis/eqc-input/control-level/longi-ctrl.csv'
    
    level_control = LevelControl(file_proj,file_ctrl).write('hello')


if __name__ == '__main__' :
    main()
