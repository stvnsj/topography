import numpy as np
import utils
import refactorModel.model as mdl
import control.model as control_model
import os

import re

def contains_cer(text):
    # Match "cer" exactly (part of a larger word)
    return bool(re.search(r'cer', text, re.IGNORECASE))

DEFAULT_STACK_LENGTH = 5

class StackElement:
    
    def __init__(self,section,f,x=900,y=900):
        
        self.section = section # Cross section to be drawn
        self.f = f # file
        
        self.x0 = utils.round_float(x) # Left border of the box
        self.y0 = utils.round_float(y) # Bottom border of the box
        
        self.minDist = np.min(np.concatenate((section.topo_dist, section.ctrl_dist)));
        self.maxDist = np.max(np.concatenate((section.topo_dist, section.ctrl_dist)));
        
        self.dist_range = self.maxDist - self.minDist;
        
        
        self.excess = 2.0 # horizontal excess
        
        # Length of horizontal structural lines.
        self.structLineLength = self.dist_range + 2 * self.excess;
        
        
        # self.maxHeight = np.max(section.topo_height)
        # self.minHeight = np.min(section.topo_height)
        self.maxHeight = np.max(np.concatenate((section.topo_height,section.ctrl_height)))
        self.minHeight = np.min(np.concatenate((section.topo_height,section.ctrl_height)))
        self.heightDelta = 10;
        self.h0 = int(self.minHeight) - 1
        
        
        # This list indexes the distance array, so that
        # the order goes from negative to positive, e.g.:
        # -17.1, ... , 0 , +15.24
        self.indexList = np.argsort(section.topo_dist)
        
        self.ctrl_sorted_index = np.argsort(section.ctrl_dist)
        
        
        
        ##################
        # Element Layout #
        ##################
        
        
        
        
        # ---------------------------------------------- y_figure
        #
        #   H1    H2    H3   ...                   Hn    y_heightNum
        #
        # ---------------------------------------------- y_heightUnderline
        #
        #   D1    D2    D3   ...                   Dn    y_distNum
        #
        # ---------------------------------------------- y_distUnderline
        
        self.y_km                        = 0.5 + self.y0
        
        self.y_topo_dist_underline       = 2.0 + self.y_km 
        self.y_topo_dist_num             = 2.1 + self.y_topo_dist_underline 
        self.y_topo_height_underline     = 2.1 + self.y_topo_dist_num 
        self.y_topo_height_num           = 2.1 + self.y_topo_height_underline
        
        self.y_ctrl_dist_underline       = 2.1 + self.y_topo_height_num
        self.y_ctrl_dist_num             = 2.1 + self.y_ctrl_dist_underline
        self.y_ctrl_height_underline     = 2.1 + self.y_ctrl_dist_num
        self.y_ctrl_height_num           = 2.1 + self.y_ctrl_height_underline  
        
        self.y_figure                    = 2.1 + self.y_ctrl_height_num
        self.y_refnum                    = 0.5 + self.y_figure 
        
        self.x_refnum                    = 0.5 + self.x0 
        self.x_labelText                 = 0.5 + self.x0 
        self.x_structLine                = 1.5 + self.x_refnum 
        self.x_figure                    = self.excess + self.x_structLine 
        self.x_num                       = self.x_figure 
        self.x_km                        = self.x_figure + np.absolute(self.minDist) 
        
        self.x0_labelBox                 = self.x_labelText - 1.5
        self.x1_labelBox                 = self.x_labelText + 1.5
        self.x_box_left                  = self.x0_labelBox -3.0     # Leftmost part of the box
        self.x_label_0                   = self.x0_labelBox -1.5     # Position of the labels 'PROYECTO' y 'CONTROL'
        
        self.y0_labelBox                 = self.y_topo_dist_underline
        self.y1_labelBox                 = self.y_topo_height_underline
        self.y2_labelBox                 = self.y_figure
        self.x_boxRight                  = self.x_structLine + self.structLineLength
        self.x1                          = self.x_structLine + self.structLineLength + 15
    

    
    def topo_ground_line (self, f):
        """Generates the surface points of the cross-section"""
        
        distance = utils.format_float_array(self.section.topo_dist[self.indexList] - self.minDist + self.x_figure);
        height   = utils.format_float_array(self.y_figure + (self.section.topo_height[self.indexList] - self.h0));
        content = np.array([d + "," + h for d, h in zip(distance, height)])[:, None]
        f.write("PLINE\n")
        np.savetxt(f, content ,fmt='%s')
        f.write("\n")
    
    
    def ctrl_ground_line (self, f):
        """Generates the surface points of the cross-section"""
        distance = utils.format_float_array(self.section.ctrl_dist[self.ctrl_sorted_index] - self.minDist + self.x_figure);
        height   = utils.format_float_array(self.y_figure + (self.section.ctrl_height[self.ctrl_sorted_index] - self.h0));
        content = np.array([d + "," + h for d, h in zip(distance, height)])[:, None]
        f.write("PLINE\n")
        np.savetxt(f, content ,fmt='%s')
        f.write("\n")
    
    
    def ctrl_height_line (self, f):
        """Generates the set of lines from the base-line to the surface"""
        distance = utils.format_float_array(self.section.ctrl_dist[self.ctrl_sorted_index] - self.minDist + self.x_figure);
        height   = utils.format_float_array(self.y_figure + (self.section.ctrl_height[self.ctrl_sorted_index] - self.h0));        
        content = np.array([
            "LINE " + d + "," + f'{utils.formatFloat(self.y_figure)} ' + d + "," + h + "\n"
            for d, h in zip(distance, height)])[:, None]
        np.savetxt(self.f, content ,fmt='%s')
        
 
 
    def axisLines (self,f):
        """Generates X and Y axis lines, baseline, and Z-axis line """
        
        x1 = utils.formatFloatArray( np.array([
            self.x_figure + np.absolute(self.minDist), # AXIS LINE
            self.x_box_left, # TOP OF THE BOX
            self.x_box_left, # BOTTOM OF THE BOX
            self.x_box_left, # Middle of the box
            self.x0_labelBox, # Middle of CTRL
            self.x0_labelBox, # Middle of TOPO
            self.x_box_left,  # Wall 1
            self.x0_labelBox, # wall 2
            self.x1_labelBox, # wall 3
            self.x_structLine + self.structLineLength, # Wall 4
        ]))
        
        y1 = utils.formatFloatArray(np.array([
            self.y_figure,  # AXIS LINE
            self.y_figure,  # TOP OF THE BOX
            self.y_topo_dist_underline, # BOTTOM OF THE BOX
            self.y_ctrl_dist_underline, #Middle of the box
            self.y_ctrl_height_underline, #Middle of CTRL
            self.y_topo_height_underline, # Middle of TOPO
            self.y_figure,  # Wall 1
            self.y_figure,  # Wall 2
            self.y_figure,  # Wall 3
            self.y_figure,  # Wall 4
        ]))
        
        x2 = utils.formatFloatArray(np.array([
            self.x_figure + np.absolute(self.minDist), # AXIS LINE
            self.x_structLine + self.structLineLength, # TOP OF THE BOX
            self.x_structLine + self.structLineLength, # BOTTOM OF THE BOX
            self.x_structLine + self.structLineLength, # MIDDLE OF THE BOX
            self.x_structLine + self.structLineLength, # Middle of CTRL
            self.x_structLine + self.structLineLength, # Middle of TOPO
            self.x_box_left,  # Wall 1
            self.x0_labelBox, # wall 2
            self.x1_labelBox, # wall 3
            self.x_structLine + self.structLineLength, # Wall 4
        ]))
        
        y2 = utils.formatFloatArray(np.array([
            self.y_figure + (self.maxHeight - self.h0) + 1,  # AXIS LINE
            self.y_figure,  # TOP OF THE BOX
            self.y_topo_dist_underline, # BOTTOM OF THE BOX
            self.y_ctrl_dist_underline, #Middle of the box
            self.y_ctrl_height_underline, #Middle of CTRL
            self.y_topo_height_underline, # Middle of TOPO
            self.y_topo_dist_underline,   # Wall 1
            self.y_topo_dist_underline,   # Wall 2
            self.y_topo_dist_underline,   # Wall 3
            self.y_topo_dist_underline,   # Wall 4
        ]))
        
        content = np.array([
            "LINE " + a + "," +  b + " " + c + "," + d + "\n"
            for a, b, c, d in zip(x1, y1, x2, y2)])[:, None]
        np.savetxt(self.f, content ,fmt='%s')
    
    
    def topo_dist_num (self,f):
        """Generates the distance numbers on the X-axis"""
        
        distance = utils.format_float_array(self.section.topo_dist[self.indexList] - self.minDist + self.x_figure);
        labels   = utils.format_float_array(self.section.topo_dist[self.indexList])
        content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_topo_dist_num) + " 0.50 90 " + l
            for d,l in zip(distance, labels)])
        np.savetxt(self.f, content ,fmt='%s')
    
    
    def ctrl_dist_num (self,f):
        """Generates the distance numbers on the X-axis"""
        
        distance = utils.format_float_array(self.section.ctrl_dist[self.ctrl_sorted_index] - self.minDist + self.x_figure);
        labels   = utils.format_float_array(self.section.ctrl_dist[self.ctrl_sorted_index])
        content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_ctrl_dist_num) + " 0.50 90 " + l
            for d,l in zip(distance, labels)])
        np.savetxt(self.f, content ,fmt='%s')
    
    
    def topo_height_num (self,f):
        """Generates the height numbers on the X-axis"""
        
        distance = utils.format_float_array(self.section.topo_dist[self.indexList] - self.minDist + self.x_figure);
        labels   = utils.format_float_array(self.section.topo_height[self.indexList])
        content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_topo_height_num) + " 0.50 90 " + l
            for d,l in zip(distance, labels)])
        np.savetxt(self.f, content ,fmt='%s')
    
    def ctrl_height_num (self,f):
        """Generates the height numbers on the X-axis"""
        
        distance = utils.format_float_array(self.section.ctrl_dist[self.ctrl_sorted_index] - self.minDist + self.x_figure);
        labels   = utils.format_float_array(self.section.ctrl_height[self.ctrl_sorted_index])
        content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_ctrl_height_num) + " 0.50 90 " + l
            for d,l in zip(distance, labels)])
        np.savetxt(self.f, content ,fmt='%s')
    
    
    def heightRef (self,f):
        """Generates the refence height text above the box"""
        
        x = utils.formatFloat(self.x_refnum)
        y = utils.formatFloat(self.y_refnum)
        d = utils.formatFloat(self.h0)
        self.f.write(f'-TEXT M {x},{y} 0.45 0 Ref: {d}\n')
        
    
    def kmLabel (self,f):
        x = utils.formatFloat(self.x_km)
        y = utils.formatFloat(self.y_km)
        self.f.write(f'-TEXT M {x},{y} 0.85 0 DM: {self.section.id}\n')


    def topo_label (self, f):
        x = utils.formatFloat(self.x_label_0)
        y = utils.formatFloat(self.y_topo_height_underline)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 PROYECTO\n')
    
    def ctrl_label (self, f):
        x = utils.formatFloat(self.x_label_0)
        y = utils.formatFloat(self.y_ctrl_height_underline)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 CONTROL\n')
    
    
    def topo_dist_label (self,f) :
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_topo_dist_num)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 DIST.\n')
    
    def ctrl_dist_label (self,f) :
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_ctrl_dist_num)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 DIST.\n')
    
    def topo_height_label (self, f) :
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_topo_height_num)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 COTA\n')
    
    def ctrl_height_label (self, f) :
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_ctrl_height_num)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 COTA\n') 
    
    def write (self):
        
        # Topographic Ground Line
        self.f.write("-LAYER N TIERRA_PROYECTO C 5 TIERRA_PROYECTO S TIERRA_PROYECTO L CONTINUOUS\n\n\n")
        self.topo_ground_line(self.f)
        
        # Control Groud Line
        self.f.write("-LAYER N TIERRA_CONTROL C 1 TIERRA_CONTROL S TIERRA_CONTROL L DASHED\n\n\n")
        self.ctrl_ground_line(self.f)
        
        ##################
        # VERTICAL LINES #
        ##################
        self.f.write("-LAYER N ALTURA_CONTROL C 252 ALTURA_CONTROL S ALTURA_CONTROL L CONTINUOUS\n\n\n")
        self.ctrl_height_line(self.f)
        
        self.f.write("-LAYER N CAJA C 1 CAJA S CAJA L CONTINUOUS\n\n\n")
        self.axisLines(self.f)
        
        self.f.write("-LAYER N DISTANCIAS C 1 DISTANCIAS S DISTANCIAS L CONTINUOUS\n\n\n")
        self.topo_dist_num(self.f)
        self.ctrl_dist_num(self.f)
     
        self.f.write("-LAYER N COTAS C 3 COTAS S COTAS L CONTINUOUS\n\n\n")
        self.topo_height_num(self.f)
        self.ctrl_height_num(self.f)
     
        self.f.write("-LAYER N REFERENCIAS C 7 REFERENCIAS S REFERENCIAS L CONTINUOUS\n\n\n")
        
        self.heightRef(self.f)
        self.kmLabel(self.f)
        
        self.topo_dist_label(self.f)
        self.ctrl_dist_label(self.f)
        self.topo_height_label(self.f)
        self.ctrl_height_label(self.f)
        self.ctrl_label(self.f)
        self.topo_label(self.f)
        return self.x1



class Stack:
    
    def __init__(self, model, y):
        
        self.x0 = 0;
        self.y0 = y;
        self.currX = self.x0
        self.km0 = ""
        self.km1 = ""
        self.model = model
    
    # i (initial sectionIndex)
    # j (end sectionIndex)
    # K 
    def write (self, f, i, j):
        
        if i >= self.model.size:    
            return ""
        
        self.km0 = self.model.getSection(i).id;
        
        iterator = control_model.ModelIterator(self.model,i,j)
        
        self.currX += 85
        
        for section in iterator:
            stackElement = StackElement(section, f, x=self.currX, y=self.y0)
            self.km1 = section.id
            self.currX = stackElement.write() 
        
        f.write("-LAYER N ENCABEZADO C 7 ENCABEZADO S ENCABEZADO L CONTINUOUS\n\n\n")
        f.write(f'-TEXT ML {self.x0},{self.y0+4} 2.50 0 PT Desde M: {self.km0}\n')
        f.write(f'-TEXT ML {self.x0},{self.y0} 2.50 0    Hasta M: {self.km1}\n')
        
        self.y0 -= 80;
        
        return self.y0




class CadScript:
    
    def __init__ (self, model):
        self.model = model;
    
    # i : Initial index of iteration
    # j : End index of iteration
    def write (self, i , j , stackSize=5.0, filename="test.txt"):
        
        y0 = 0.000
        
        with open(filename, "w") as f:
            
            while True:
                
                # This is the case where the stacksize
                # can be fully written.
                # i = 0 ; j = 13 ; stacksize = 5
                # 0 + 5 - 1 < 14 ===> 
                # i = 5 ; j = 13 ; stacksize = 5
                if  i + stackSize - 1 < j :
                    stack = Stack(self.model, y0)
                    y0 = stack.write(f, i, i + stackSize - 1)
                    i += stackSize;
                
                
                else:
                    stack = Stack(self.model, y0)
                    stack.write(f, i, j)
                    break
    
    
    def writeKm (self,dm0="",dm1="", stackSize=5, fn="testcadkm.SCR"):
        
        i = self.model.get_lower_dm_index(dm0)
        j = self.model.get_upper_dm_index(dm1)
        self.write(i,j, stackSize, fn)
    
    
    # fileSize is the number of cross sections per file
    def writeFull (self, path, project_name, fileSize = 30, stackSize = 5):
        
        N = self.model.size
        directory = os.path.join(path,project_name)
        os.makedirs(directory, exist_ok=True)
        
        for k in range(0,N,fileSize):
            
            if k < N:
                
                km = self.model.getSection(k).km
                
                file_path = os.path.join(directory, f"{project_name}-{km}.scr")
                
                self.write(
                    k,
                    k+fileSize-1,
                    stackSize=stackSize,
                    filename = file_path
                )
            
            else:
                break
    
    def writeCompleteProject(self, filename, stackSize=5):
        N = self.model.get_size()
        self.write(0, N , stackSize=stackSize, filename=filename)


def main():
    print("Refactor CAD")
    
    coor_topo = "/home/jstvns/axis/eqc-input/auto-control/coor-topo.csv"
    coor_ctrl = "/home/jstvns/axis/eqc-input/auto-control/coor-ctrl.csv"
    longitudinal = "/home/jstvns/axis/eqc-input/auto-control/longitudinal.csv"
    
    model1 = mdl.Model(
        filename1 = "", # DESCR
        filename2 = coor_topo, # COOR
        filename3 = longitudinal, # LONG
    )
    
    model2 = mdl.Model(
        filename1 = "",
        filename2 = coor_ctrl,
        filename3 = longitudinal,
    )
    
    cmodel = control_model.ControlModel(model1,model2)
    
    scr = CadScript(cmodel)
    
    # scr.writeCompleteProject("test.scr")
    
    scr.writeKm (dm0="5000",dm1="5789.800",stackSize=3,fn="CONTROL_TEST.scr")



if __name__ == "__main__":
    main()
