import numpy as np
import utils
from control.mop import MOP
from control.range import ControlRangeList
import sys
import os

DEFAULT_STACK_LENGTH = 5

class StackElement:
    
    def __init__(self, sec_proj=None, sec_ctrl=None, f=None, x=900, y=900):
        
        self.sec_proj = sec_proj
        self.sec_ctrl = sec_ctrl
        
        
        self.f = f # file
        
        self.x0 = utils.round_float(x) # Left border of the box
        self.y0 = utils.round_float(y) # Bottom border of the box
        
        self.minDist = min(sec_proj.get_min_dist(), sec_ctrl.get_min_dist()).distance
        self.maxDist = max(sec_proj.get_max_dist(), sec_ctrl.get_max_dist()).distance
        
        self.dist_range = self.maxDist - self.minDist;
        
        self.excess = 2.0 # horizontal excess
        
        # Length of horizontal structural lines.
        self.structLineLength = self.dist_range + 2 * self.excess;
        
        
        self.minHeight = min(sec_proj.get_min_height(), sec_ctrl.get_min_height()).height
        self.maxHeight = max(sec_proj.get_max_height(), sec_ctrl.get_max_height()).height
        
        self.heightDelta = 10;
        self.h0 = int(self.minHeight) - 1
        
        
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
        
        self.proj_dist_arr               = np.array([p.distance for p in self.sec_proj.point_list])
        self.ctrl_dist_arr               = np.array([p.distance for p in self.sec_ctrl.point_list])
        
        self.proj_height_arr             = np.array([p.height   for p in self.sec_proj.point_list])
        self.ctrl_height_arr             = np.array([p.height   for p in self.sec_ctrl.point_list])
    
    
    def ground_line_proj (self, f):
        """Generates the surface points of the cross-section"""
        
        distance = utils.format_float_array(self.proj_dist_arr - self.minDist + self.x_figure);
        height   = utils.format_float_array(self.y_figure + (self.proj_height_arr - self.h0));
        content = np.array([d + "," + h for d, h in zip(distance, height)])[:, None]
        f.write("PLINE\n")
        np.savetxt(f, content ,fmt='%s')
        f.write("\n")
    
    
    def ground_line_ctrl (self, f):
        if self.sec_ctrl is None:
            return
        """Generates the surface points of the cross-section"""
        distance = utils.format_float_array(self.ctrl_dist_arr - self.minDist + self.x_figure);
        height   = utils.format_float_array(self.y_figure + (self.ctrl_height_arr - self.h0));
        content = np.array([d + "," + h for d, h in zip(distance, height)])[:, None]
        f.write("PLINE\n")
        np.savetxt(f, content ,fmt='%s')
        f.write("\n")
    
    
    def height_line_ctrl (self, f):
        if self.sec_ctrl is None:
            return
        """Generates the set of lines from the base-line to the surface"""
        distance = utils.format_float_array(self.ctrl_dist_arr - self.minDist + self.x_figure);
        height   = utils.format_float_array(self.y_figure + (self.ctrl_height_arr - self.h0));        
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
    
    
    def dist_num_proj (self,f):
        """Generates the distance numbers on the X-axis"""
        
        distance = utils.format_float_array(self.proj_dist_arr - self.minDist + self.x_figure);
        labels   = utils.format_float_array(self.proj_dist_arr)
        content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_topo_dist_num) + " 0.50 90 " + l
            for d,l in zip(distance, labels)])
        np.savetxt(self.f, content ,fmt='%s')
    
    
    def dist_num_ctrl (self,f):
        """Generates the distance numbers on the X-axis"""
        
        distance = utils.format_float_array(self.ctrl_dist_arr - self.minDist + self.x_figure);
        labels   = utils.format_float_array(self.ctrl_dist_arr)
        content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_ctrl_dist_num) + " 0.50 90 " + l
            for d,l in zip(distance, labels)])
        np.savetxt(self.f, content ,fmt='%s')
    
    
    def height_num_proj (self,f):
        """Generates the height numbers on the X-axis"""
        distance = utils.format_float_array(self.proj_dist_arr - self.minDist + self.x_figure);
        labels   = utils.format_float_array(self.proj_height_arr)
        content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_topo_height_num) + " 0.50 90 " + l
            for d,l in zip(distance, labels)])
        np.savetxt(self.f, content ,fmt='%s')
    
    def height_num_ctrl (self,f):
        """Generates the height numbers on the X-axis"""
        distance = utils.format_float_array(self.ctrl_dist_arr - self.minDist + self.x_figure);
        labels   = utils.format_float_array(self.ctrl_height_arr)
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
        
    
    def dm_label (self,f):
        x = utils.formatFloat(self.x_km)
        y = utils.formatFloat(self.y_km)
        self.f.write(f'-TEXT M {x},{y} 0.85 0 DM: {self.sec_proj.dm}\n')


    def label_proj (self, f):
        x = utils.formatFloat(self.x_label_0)
        y = utils.formatFloat(self.y_topo_height_underline)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 PROYECTO\n')
    
    def label_ctrl (self, f):
        x = utils.formatFloat(self.x_label_0)
        y = utils.formatFloat(self.y_ctrl_height_underline)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 CONTROL\n')
    
    
    def dist_label_proj (self,f) :
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_topo_dist_num)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 DIST.\n')
    
    def dist_label_ctrl (self,f) :
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_ctrl_dist_num)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 DIST.\n')
    
    def height_label_proj (self, f) :
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_topo_height_num)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 COTA\n')
    
    def height_label_ctrl (self, f) :
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_ctrl_height_num)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 COTA\n') 
    
    def write (self):
        
        # Topographic Ground Line
        self.f.write("-LAYER N TIERRA_PROYECTO C 5 TIERRA_PROYECTO S TIERRA_PROYECTO L CONTINUOUS\n\n\n")
        self.ground_line_proj(self.f)
        
        # Control Groud Line
        self.f.write("-LAYER N TIERRA_CONTROL C 1 TIERRA_CONTROL S TIERRA_CONTROL L DASHED\n\n\n")
        self.ground_line_ctrl(self.f)
        
        ##################
        # VERTICAL LINES #
        ##################
        self.f.write("-LAYER N ALTURA_CONTROL C 252 ALTURA_CONTROL S ALTURA_CONTROL L CONTINUOUS\n\n\n")
        self.height_line_ctrl(self.f)
        
        self.f.write("-LAYER N CAJA C 1 CAJA S CAJA L CONTINUOUS\n\n\n")
        self.axisLines(self.f)
        
        self.f.write("-LAYER N DISTANCIAS C 1 DISTANCIAS S DISTANCIAS L CONTINUOUS\n\n\n")
        self.dist_num_proj(self.f)
        self.dist_num_ctrl(self.f)
     
        self.f.write("-LAYER N COTAS C 3 COTAS S COTAS L CONTINUOUS\n\n\n")
        self.height_num_proj(self.f)
        self.height_num_ctrl(self.f)
     
        self.f.write("-LAYER N REFERENCIAS C 7 REFERENCIAS S REFERENCIAS L CONTINUOUS\n\n\n")
        
        self.heightRef(self.f)
        self.dm_label(self.f)
        
        self.dist_label_proj(self.f)
        self.dist_label_ctrl(self.f)
        self.height_label_proj(self.f)
        self.height_label_ctrl(self.f)
        self.label_ctrl(self.f)
        self.label_proj(self.f)
        return self.x1



class Stack:
    
    def __init__(self, mop_proj, mop_ctrl, dm_list, y):
        
        self.x0 = 0;
        self.y0 = y;
        self.currX = self.x0
        self.km0 = ""
        self.km1 = ""
        
        self.mop_proj = mop_proj
        self.mop_ctrl = mop_ctrl
        self.dm_list  = dm_list
        
    
    def write (self, f, i, j):
        
        if i >= len(self.dm_list):    
            return 0
        
        
        
        # self.km0 = self.model.getSection(i).id;
        self.km0 = self.dm_list[i];
        
        self.currX += 85
        
        for dm in self.dm_list[i:j+1]:
            proj_section = self.mop_proj.get_section(dm)
            ctrl_section = self.mop_ctrl.get_section(dm)
            stackElement = StackElement(proj_section,ctrl_section,f,x=self.currX, y=self.y0)
            self.km1 = dm
            self.currX = stackElement.write()
        
        f.write("-LAYER N ENCABEZADO C 7 ENCABEZADO S ENCABEZADO L CONTINUOUS\n\n\n")
        f.write(f'-TEXT ML {self.x0},{self.y0+4} 2.50 0 PT Desde M: {self.km0}\n')
        f.write(f'-TEXT ML {self.x0},{self.y0} 2.50 0    Hasta M: {self.km1}\n')
        
        self.y0 -= 80;
        
        return self.y0




class CadScript:
    
    def __init__ (self, filename_proj, filename_ctrl):
        
        self.mop_proj = MOP(filename_proj)
        self.mop_ctrl = MOP(filename_ctrl)
        
        self.project_dm_list = self.mop_proj.get_dm_list()
        self.control_dm_list = self.mop_ctrl.get_dm_list()
        self.dm_list         = sorted(
            np.intersect1d(self.project_dm_list,self.control_dm_list),
            key = float
        )
    
    
    # i : Initial index of iteration
    # j : End index of iteration
    def write (self,stackSize=5, filename="test.txt"):
        
        y0 = 0.000
        i  = 0
        j  = len(self.project_dm_list) - 1
        
        with open(filename, "w") as f:
            
            while True:
                
                if  i + stackSize - 1 < j :
                    stack = Stack(self.mop_proj,self.mop_ctrl,self.dm_list, y0) #!!!!!
                    y0 = stack.write(f, i, i + stackSize - 1)
                    i += stackSize;
                
                else:
                    stack = Stack(self.mop_proj,self.mop_ctrl,self.dm_list, y0)
                    stack.write(f, i, j)
                    break

def main(input1,input2,output):
    print("Refactor CAD")
    cad = CadScript(input1,input2)
    cad.write(filename=output)

if __name__ == "__main__":
    main(sys.argv[1],# MOP TOPO
         sys.argv[2],# MOP CTRL
         sys.argv[3])# OUTPUT
