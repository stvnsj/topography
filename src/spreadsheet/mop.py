
import numpy as np
import refactorModel.model as mdl
import utils


class MopFormat :
    
    def __init__ (self, model) :
        self.__model = model
    
    
    def write_section (self,section,f) :
        
        ascendingIndex = np.argsort(section.distance[1:])
        section.distance[1:] = section.distance[1:][ascendingIndex]
        section.coor_x[1:] = section.coor_x[1:][ascendingIndex]
        section.coor_y[1:] = section.coor_y[1:][ascendingIndex]
        
        descendingIndex = np.argsort(np.where(section.distance[1:]<0)[0])[::-1]
        
        # Index of the last negative number 
        neg = len(descendingIndex)
        
        # reversed ordered on negative part of distance
        section.distance[1:neg+1] = section.distance[1:][descendingIndex]
        section.coor_x[1:neg+1]   = section.coor_x[1:][descendingIndex]
        section.coor_y[1:neg+1]   = section.coor_y[1:][descendingIndex]
        
        section.adjustedHeight[1:] = section.adjustedHeight[1:][ascendingIndex]
        section.adjustedHeight[1:neg+1] = section.adjustedHeight[1:][descendingIndex]
        
        section.labels[1:] = section.labels[1:][ascendingIndex]
        section.labels[1:neg+1] = section.labels[1:][descendingIndex]
        
        section.labels[0] = '0ep'
        
        section.side[1:] = section.side[1:][ascendingIndex]
        section.side[1:neg+1] = section.side[1:][descendingIndex]
        
        full_table = np.empty((0, 6))
        
        content = np.column_stack((
            # np.where(np.isnan(section.matrix[:,[0]]),'',section.matrix[:,[0]].astype(str)),
            section.matrix[:,0],
            utils.format_float_array (section.distance),
            utils.format_float_array (section.adjustedHeight),
            section.labels,
        ))
        np.savetxt(f,content,delimiter=',',fmt='%s')
    
    
    def write (self,filename="testmop.csv") :
        END = self.__model.size + 1
        
        sections = mdl.ModelIterator(self.__model,0,END+1)
        
        with open(filename, "w") as f:
            for section in sections :
                self.write_section(section,f)
