import numpy as np
from refactorModel.section import Section
import utils
import sys
import os
import common.numeric as numeric



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


class Iterator :
    
    def __init__ (self, model):
        self.__model__ = model
        self.__index__ = 0
    
    def __iter__ (self) :
        return self
    
    def __next__ (self) :
        if self.__index__ >= self.__model__.size:
            raise StopIteration
        section = self.__model__.getSection(self.__index__)
        self.__index__ += 1
        return section
        

class Model :
    def __init__ (
            self,
            filename1 = "", # Descriptor File
            filename2 = "", # Coordinate File
            filename3 = "", # Longitudinal File
    ):
        print('refactorModel')
        
        # This calls should be abstracted.
        matrix_descr  = utils.read_csv(filename1) if filename1 != "" else None
        matrix_coor   = utils.read_csv(filename2) if filename2 != "" else None 
        matrix_height = utils.read_csv(filename3,cols=(0,1)) if filename3 != "" else None
        
        #######################
        # PRINT FILE MESSAGES #
        #######################
        if (filename1 == "") and (filename2 == "") :
            print(">> Error: Se ha cargado ningún archivo transversal")
            return
        if (filename3 == "") :
            print(">> Advertencia: No se ha cargado un archivo longitudinal")
        

        # This dictionary contains the precise height of the DM in the project.
        self.heights = dict(matrix_height) if filename3 else {}
        
        # list of cross sections of this model
        self.sections = [] # [Section]
        self.sectionIndex = [] # [Int]
        
        # oriented cross sections are build and oriented
        if matrix_coor is not None:
            self.build_section(matrix_coor,oriented=True, true_z=True if filename3 else False)
            self.sections.sort()
            self.reference_vector()
        
        if matrix_descr is not None:
            self.build_section(matrix_descr,oriented=False, true_z = True if filename3 else False)
            
        self.distance_sign()
        self.sections.sort()
        self.deduplicate()
        self.currSection = 0
        self.size = len(self.sectionIndex)
        self.dm_index = {}
        self.dms = []
        self.__init_dms__()
        self.__init_dm_index__()
    
 
    def __init_dms__ (self):
        for i in range(self.size):
            self.dms.append(self.getSection(i).km)
    
    def __init_dm_index__ (self) :
        self.dm_index = {self.getSection(i).km : i for i in range(self.size)}
    
    def deduplicate (self) :
        
        i = 0
        j = 1
        
        length = len(self.sections)
        
        
        self.sectionIndex.append(i)
        
        # For all j 
        while j < length :
            # If both sections are equal,
            if self.sections[i] == self.sections[j]:
                # Append section j to section i
                self.sections[i].merge(self.sections[j])
                j = j + 1
            # Otherwise, insert the index of section j
            # to self.sectionIndex, and 
            else:
                i = j
                j = j + 1
                self.sectionIndex.append(i)
                
    
    def get_km_index_dict (self):
        d = {self.getSection(i).km : i for i in range(len(self.sectionIndex))}
        return d
    
    


    def guessHeight(self, km):
        dm_float = numeric.to_rounded_float(km)
        if dm_float is None:
            print(f'No hay cambio sugerido para {km}')
            return

        for dm0 in self.heights:
            dm0_float = numeric.to_rounded_float(dm0)
            if dm0_float is None:
                continue

            if numeric.are_close(dm_float, dm0_float, tolerance=0.01):
                print(f'Cambio sugerido: {km} --> {dm0}')
                return

        print(f'No hay cambio sugerido para {km}')

    def findHeight(self, dm, default=0):
        if dm not in self.heights:
            print(f'>> Advertencia: DM {dm} no se encuentra en el archivo Longitudinal')
            self.guessHeight(dm)
            return default

        height = self.heights[dm]

        if numeric.to_float(height) is None:
            print(f'>> Advertencia: DM {dm} presenta un error en el archivo longitudinal')
            return default

        return height
    
    
    def reference_vector(self):
        N = len(self.sections)
        for i in range(0,N):
            for d in range (1,N):
                if i + d < N :
                    if self.sections[i+d].km != self.sections[i].km:
                        axis1 = utils.str_to_flt_arr(self.sections[i].axis)
                        axis2 = utils.str_to_flt_arr(self.sections[i+d].axis)
                        self.sections[i].vector = axis2 - axis1
                        break
                if i - d >= 0:
                    if self.sections[i-d].km != self.sections[i].km:
                        axis1 = utils.str_to_flt_arr(self.sections[i].axis)
                        axis0 = utils.str_to_flt_arr(self.sections[i-d].axis)
                        self.sections[i].vector = axis1 - axis0
                        break
    
    def get_size(self):
        """Returns the number of non-duplicate cross sections in the model"""
        return len(self.sectionIndex)
    
    def distance_sign (self):
        "Compute the signs of the model's sections"
        for sec in self.sections:
            sec.compute_sign()
    
    def getSection(self,index):
        "Get a section by its index number"
        i = self.sectionIndex[index]
        return self.sections[i]


    def build_section (self,matrix,oriented=True,true_z = True): 
        start = 0 # start index of matrix chunk copied
        end = 0 # end index of matrix chunk copied
        i = 1 # pointer to traverse the matrix 
        length = matrix.shape[0] # vertical size of matrix
        
        while i < length :
            
            # If the value of km is nan, then keep stacking more
            # points to the current section
            if matrix[i][0] == "" :
                end = end + 1;
                i   = i + 1
                
                if(i == length):
                    
                    height = self.findHeight(matrix[start][0],default=matrix[start][3]) if true_z else matrix[start][3]
                    
                    section = Section(
                        matrix[start][0],
                        matrix[start:end+1],
                        matrix[start:end+1,4],
                        height,
                        axis = matrix[start,1:3],
                        oriented = oriented
                    )
                    
                    self.sections.append(section)
            
            
            elif matrix[i][0] != "" :
                
                end = end + 1;
                height = self.findHeight(matrix[start][0],default=matrix[start][3]) if true_z else matrix[start][3]
                section = Section(
                    matrix[start][0],
                    matrix[start:end],
                    matrix[start:end,4],
                    height,
                    axis = matrix[start, 1:3],
                    oriented = oriented
                )  
                self.sections.append(section)
                start = i
                end = i
                i = i + 1
    
    
 
    def get_lower_dm_index(self, dm = "0.000"):
        """Returns the minumum index with a dm greater than or equal to the argument"""
        N = len(self.sectionIndex)
        if dm == "0.000":
            return 0
        for j in range(N):
            if float(self.getSection(j).km) >= float(dm):
                return j
            j += 1
        return 0
    
    def get_upper_dm_index(self,dm = "0.000"):
        N = len(self.sectionIndex)
        if dm == "0.000":
            return N - 1
        for j in range (N):
            if float(self.getSection(j).km) > float(dm):
                return j-1
            j += 1
        return N - 1
 
    def getKmRange(self,dm0,dm1):
        """Translates a range of dm's to a range of sectionIndex indices"""
        
        if np.float64(dm0) >= np.float64(dm1) :
            raise utils.CustomError("El dm inferior debe ser menor que el dm superior")
        
        i0 = 0 # Start Index
        i1 = self.size - 1 # End Index
        
        i = 0
        itr = ModelIterator(self)
        
        for section in itr:
            
            if np.float64(section.km) >= np.float64(dm0):
                
                i0 = i
                break
            
            else:
                i += 1
        
        itr2 = ModelIterator(self, i0)
        
        for section in itr2:
            
            if np.float64(section.km) <= np.float64(dm1):
                
                i += 1
            
            else:
                
                i1 = i-1
                break
        
        return (i0,i1)






def main ():
    
    filename1 = "/home/jstvns/eqc-input/dbase-input/dat-et-descr.csv"
    filename2 = "/home/jstvns/eqc-input/auto-control/coor-ctrl.csv"
    filename3 = "/home/jstvns/eqc-input/dbase-input/longitudinal.csv"
    
    model = Model(
        filename1 = "", # DESCR
        filename2 = filename2, # COOR
        filename3 = "", # LONG
    )




if __name__ == "__main__":
    main()


