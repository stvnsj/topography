import numpy as np
import refactorModel.model as mdl
import utils


class ModelWidth :
    
    def __init__ (self, model) :
        self.__model = model
    
    
    def write_section (self, section, f) :
        
        minIndex = np.argmin(section.distance)
        maxIndex = np.argmax(section.distance)
        
        minDistance = section.distance[minIndex]
        maxDistance = section.distance[maxIndex]        
        
        leftLabel  = 'T' if minDistance < -20.0 else ''
        rightLabel = 'T' if maxDistance > 20.0  else ''
        
        content = np.array([[
            section.km,
            utils.format_float_array(minDistance),
            utils.format_float_array(maxDistance),
            leftLabel,
            rightLabel
        ]])
        
        np.savetxt(f, content, delimiter=',', fmt='%s')
    
    
    def write (self, filename="testwidth.csv") :
       	
       	END = self.__model.size + 1
        
        sections = mdl.ModelIterator(self.__model,0,END+1)
        
        with open(filename, "w") as f:
            for section in sections :
                self.write_section(section,f)
