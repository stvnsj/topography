
import numpy as np
import model as mdl
import utils


class Spreadsheet :
    
    def __init__ (self, model) :
        self.__model = model
    
    
    def writeSectionMOP (self,section,f) :
        
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
        
        content = np.hstack((
            np.where(np.isnan(section.matrix[:,[0]]),'',section.matrix[:,[0]].astype(str)),
            utils.format_float_array (section.coor_x),
            utils.format_float_array (section.coor_y),
            utils.format_float_array (section.distance[:,None]),
            utils.format_float_array (section.adjustedHeight),
            section.labels[:,None],
        ))
        np.savetxt(f,content,delimiter=',',fmt='%s')
    
    
    def writeSectionWidth (self, section, f) :
        
        minIndex = np.argmin(section.distance)
        maxIndex = np.argmax(section.distance)
        
        minDistance = section.distance[minIndex]
        maxDistance = section.distance[maxIndex]        
        
        leftLabel = 'T' if minDistance < -20.0 else ''
        rightLabel = 'T' if maxDistance > 20.0 else ''
        
        content = np.array([[
            section.km,
            utils.format_float_array(minDistance),
            utils.format_float_array(maxDistance),
            leftLabel,
            rightLabel]])
        
        np.savetxt(f, content, delimiter=',', fmt='%s')
    
    
    
    def writeMOP (self,filename="testmop.csv",i=0,j=0) :
        END = self.__model.size + 1
        
        sections = mdl.ModelIterator(self.__model,0,END+1)
        
        with open(filename, "w") as f:
            np.savetxt(f, np.array([["DM","X","Y","DIST","Z","DESCR"]]), delimiter=',', fmt='%s')
            for section in sections :
                self.writeSectionMOP(section,f)
    
    
    def writeWidth (self, filename="testwidth.csv",i=0,j=0) :
       	END = self.__model.size + 1
        
        sections = mdl.ModelIterator(self.__model,0,END+1)
        
        with open(filename, "w") as f:
            for section in sections :
                self.writeSectionWidth(section,f)
    
    def writeKmMOP (self,fn="testmoprange.csv",km0="0",km1="0"):
        i,j = self.__model.getKmRange(km0,km1)
        self.writeMOP(fn,i,j)
    
    def writeKmWidth (self, fn="testwidthrange.csv", km0="0" , km1="0"):
        i,j = self.__model.getKmRange(km0,km1)
        self.writeWidth(fn,i,j)


