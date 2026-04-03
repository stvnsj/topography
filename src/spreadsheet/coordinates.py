
import numpy as np
import refactorModel.model as mdl
import utils


class AdjustedCoordinateModel :
    
    def __init__ (self, model) :
        self.__model = model
        self.__index = 1
    
    
    def writeSection (self,section,f) :
        
        ascendingIndex       = np.argsort(section.distance[1:])
        section.distance[1:] = section.distance[1:][ascendingIndex]
        section.coor_x[1:]   = section.coor_x[1:][ascendingIndex]
        section.coor_y[1:]   = section.coor_y[1:][ascendingIndex]
        
        descendingIndex = np.argsort(np.where(section.distance[1:]<0)[0])[::-1]
        
        # Index of the last negative number 
        neg = len(descendingIndex)
        
        # reversed ordered on negative part of distance
        section.coor_x[1:neg+1]   = section.coor_x[1:][descendingIndex]
        section.coor_y[1:neg+1]   = section.coor_y[1:][descendingIndex]
        
        section.adjustedHeight[1:] = section.adjustedHeight[1:][ascendingIndex]
        section.adjustedHeight[1:neg+1] = section.adjustedHeight[1:][descendingIndex]
        
        section.labels[1:] = section.labels[1:][ascendingIndex]
        section.labels[1:neg+1] = section.labels[1:][descendingIndex]
        
        point_number = np.arange(self.__index , self.__index + len(section.coor_x))
        self.__index += len(section.coor_x)
        
        content = np.column_stack((
            point_number,
            section.coor_x,
            section.coor_y,
            utils.format_float_array (section.adjustedHeight),
            section.labels,
        ))
        
        np.savetxt(f,content,delimiter=',',fmt='%s')
 
    
    def writeCsv (self,filename="testmop.csv") :
        END = self.__model.size + 1
        
        sections = mdl.ModelIterator(self.__model)
        
        with open(filename, "w") as f:
            for section in sections :
                self.writeSection(section,f)
    

def main () :
    coor_topo = "/home/jstvns/eqc-input/auto-control/coor-topo.csv"
    coor_ctrl = "/home/jstvns/eqc-input/auto-control/coor-ctrl.csv"
    longitudinal = "/home/jstvns/eqc-input/auto-control/longitudinal.csv"
    
    model1 = mdl.Model(
        filename1 = "", # DESCR
        filename2 = coor_topo, # COOR
        filename3 = longitudinal, # LONG
    )
    
    coordinate_model = AdjustedCoordinateModel(model1)
    coordinate_model.writeCsv("Test-Z-coordinates.csv")
    
    

if __name__ == "__main__":
    main()

