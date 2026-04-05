
import refactorModel.model as mdl
import numpy as np
import utils
from pprint import pprint
from control.tolerance import within_tol


# Incorporate a range table to the distance control.


class ModelIterator :
    def __init__ (self, model, start=0, end=0):
        self._model = model
        self._index = start
        self._end   = model.size if end==0 else end
        
    def __iter__ (self) :
        return self
    
    def __next__ (self) :
        """In this model of iteration, the upper index is included in
        the iteration"""
        if self._index >= self._model.size or self._index > self._end:
            raise StopIteration
        section = self._model.getSection(self._index)
        self._index += 1
        return section

class Line :
    
    def __init__(self,x0,y0,x1,y1):
        # PUNTOS DE PROYECTO
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        # PENDIENTE DE LA RECTA
        self.slope = (y1-y0) / (x1-x0)
    
    def get_y (self,x) :
        y = np.round(self.slope * (x - self.x0) + self.y0, 3) # Redondeado
        # y = self.slope * (x - self.x0) + self.y0 # Sin redondear
        return y
    
    def contains_x (self,x) :
        return (self.x0 <= x and x <= self.x1)
    
    def __str__ (self):
        return f'x0={self.x0}  \t x1={self.x1}\ny0={self.y0}  \ty1={self.y1}'
    
    
    
class ControlSection :
    """This is a section of the control model. It contains info about
    the control and projec measurements. It is used by the control.cad
    module"""
    def __init__ (
            self,
            dm,
            matrix,
            is_control,
            topo_distance,
            topo_height,
            ctrl_distance,
            ctrl_height
    ):
        self.matrix         = matrix
        self.is_control     = is_control
        self.dm             = dm
        self.id             = dm
        self.km             = dm
        
        self.topo_dist  = topo_distance
        self.topo_height    = topo_height
        self.ctrl_dist  = ctrl_distance
        self.ctrl_height    = ctrl_height

class TopoSection :
    
    def __init__ (self, dm, dist, height):
        self.dm = dm
        self.id = dm
        self.km = dm
        self.dist = dist
        self.height = height
        self.lines = []
        self.size = len(dist)
        self.__init_lines__()
    
    def __init_lines__ (self) :
        for i in range(1, self.size):
            x0 = self.dist[i-1]
            y0 = self.height[i-1]
            x1 = self.dist[i]
            y1 = self.height[i]
            self.lines.append(Line(x0,y0,x1,y1))
    
    def get_line(self,x):
        """Given an x value, returns the line encompassing it."""
        for line in self.lines:
            if line.contains_x(x):
                return line
        return None


# KOKOMAT 
class ControlModel :
    
    def __init__ (self, filename_proj, filename_ctrl, filename_range = ""):
        
        f1 = "/home/jstvns/eqc-input/auto-control/coor-topo.csv"
        f2 = "/home/jstvns/eqc-input/auto-control/coor-ctrl.csv"
        
        model_proj = mdl.Model.from_files(filename2 = f1)
        model_ctrl = mdl.Model.from_files(filename2 = f2)
        
        self.model_topo = model_proj
        self.model_ctrl = model_ctrl
        self.topo_sections = []
        self.ctrl_sections = []
        
        self.sections = []
        
        self.fieldNumber = 8
        
        
        for section in mdl.ModelIterator(model_proj):
            dist = np.copy (section.distance)
            height   = np.copy (section.adjustedHeight)
            sorted_indices = np.argsort(dist)
            dist[:] = dist[sorted_indices]
            height[:] = height[sorted_indices]
            dm = section.km
            self.topo_sections.append(TopoSection(dm,dist,height))
        
        for topo_sec in self.topo_sections:
            
            try:
                is_control = []
                index = model_ctrl.dm_index[topo_sec.dm]
                section = model_ctrl.getSection(index)
                is_control = []
                matrix   = np.empty((0,self.fieldNumber))
                
                for i , (x,y) in enumerate(zip(section.distance, section.adjustedHeight)):
                    
                    line = topo_sec.get_line(x)
                    
                    DM           = topo_sec.dm if i == 0 else ""
                    DIST_CTRL    = utils.formatFloat(x)
                    HEIGHT_CTRL  = utils.formatFloat(y)
                    DESCRIPTOR   = utils.clean_descriptor(section.labels[i])
                    
                    if line:
                        HEIGHT_INTER = utils.formatFloat(line.get_y(x))
                        DIFFERENCE   = utils.formatFloat(y - line.get_y(x))
                        IS_CTRL      = "1"
                        OK           = "DT" if within_tol(DESCRIPTOR, y, line.get_y(x)) else "FT"
                        is_control.append(True)
                        
                    else:
                        HEIGHT_INTER = ""
                        DIFFERENCE   = ""
                        IS_CTRL      = "0"
                        OK           = ""
                        is_control.append(False)
                        
                    new_row = np.array([DM,DIST_CTRL,HEIGHT_CTRL,DESCRIPTOR ,HEIGHT_INTER,DIFFERENCE,IS_CTRL,OK])
                    matrix  = np.vstack((matrix, new_row))
                    
                self.sections.append(
                    ControlSection(
                        topo_sec.dm,
                        matrix,
                        is_control,
                        topo_sec.dist,
                        topo_sec.height,
                        section.distance,
                        section.adjustedHeight,
                    )
                )

            except:
                print(f'DM topográfico {topo_sec.dm} no está en tramo de control.')
                continue
        
        self.size = len(self.sections)
    
    def getSection(self,i) :
        return self.sections[i]
    def get_size(self):
        return self.size()
    
    def get_lower_dm_index(self, dm = "0.000"):
        """Returns the minumum index with a dm greater than or equal to the argument"""
        N = self.size
        if dm == "0.000":
            return 0
        for j in range(N):
            if float(self.getSection(j).km) >= float(dm):
                return j
            j += 1
        return 0
    
    def get_upper_dm_index(self,dm = "0.000"):
        N = self.size
        if dm == "0.000":
            return N - 1
        for j in range (N):
            if float(self.getSection(j).km) > float(dm):
                return j-1
            j += 1
        return N - 1


def main () :
    
    f1 = "/home/jstvns/eqc-input/auto-control/coor-topo.csv"
    f2 = "/home/jstvns/eqc-input/auto-control/coor-ctrl.csv"
    
    model_topo = mdl.Model.from_files(filename2 = f1)
    model_ctrl = mdl.Model.from_files(filename2 = f2)
    
    model = ControlModel(model_topo,model_ctrl)
    
    for section in model.sections:
        pprint(section.matrix)



if __name__ == "__main__":
    main()
