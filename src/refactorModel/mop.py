import numpy as np
import utils
import sys
import os
import refactorModel.model as mdl








class Point :
    def __init__ (self,  distance, height):
        self.distance = distance
        self.height   = height
    
    def __str__ (self):
        print(f"POINT: d = {self.distance} , h = {self.height}")
        return ''

class Section :
    
    def __init__ (self,sec):
        self.dm = sec.id
        self.point_list = []
        for d , h in zip (sec.distance, sec.adjustedHeight):
            point = Point(d,h)
            self.point_list.append(point)
    
    def __str__ (self):
        for p in self.point_list:
            print(p)
        return ''

class MOP :
    
    def __init__(self, model):
        self.model = model
        self.section_list = []
        self.__init_section_list__()
        self.size = len(self.section_list) 
    
    def __init_section_list__ (self):
        for sec in mdl.Iterator(self.model):
            section = Section(sec)
            self.section_list.append(section)
    
    def __str__ (self):
        for sec in self.section_list:
            print(sec)
        return ""


def main () :
    
    desc_file = "/home/jstvns/axis/eqc-input/model/dat-et.csv"
    long_file = "/home/jstvns/axis/eqc-input/model/longitudinal.csv"
    
    model = mdl.Model(
        filename1 = desc_file,
        filename3 = long_file
    )
    
    mop = MOP(model)
    
if __name__ == "__main__":
    main()
