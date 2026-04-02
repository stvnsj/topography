import numpy as np
import utils
import model as mdl
import os




DEFAULT_STACK_LENGTH = 5



class StackElement:
    
    def __init__(self,section,f,x=900,y=900):
        
        self.section = section # Cross section to be drawn
        self.f = f # file
        
        self.x0 = utils.round_float(x) # Left border of the box
        self.y0 = utils.round_float(y) # Bottom border of the box
        
        self.minDist = np.min(section.distance);
        self.maxDist = np.max(section.distance);
        
        self.dist_range = self.maxDist - self.minDist;
        
        
        self.excess = 2.0 # horizontal excess
        
        # Length of horizontal structural lines.
        self.structLineLength = self.dist_range + 2 * self.excess;
        
        
        self.maxHeight = np.max(section.adjustedHeight)
        self.minHeight = np.min(section.adjustedHeight);
        self.heightDelta = 10;
        self.h0 = int(self.minHeight) - 1
        
        
        # This list indexes the distance array, so that
        # the order goes from negative to positive, e.g.:
        # -17.1, ... , 0 , +15.24
        self.indexList = np.argsort(section.distance);
        
        
        
        ##################
        # Element Layout #
        ##################
        
        self.y_km                  = 0.5 + self.y0  #DONE
        self.y_distUnderline       = 2.0 + self.y_km #DONE
        self.y_distNum             = 2.1 + self.y_distUnderline #DONE
        self.y_heightUnderline     = 2.1 + self.y_distNum #DONE
        self.y_heightNum           = 2.1 + self.y_heightUnderline #DONE
        self.y_figure              = 2.1 + self.y_heightNum #DONE
        self.y_refnum              = 0.5 + self.y_figure #DONE
        
        self.x_refnum              = 0.5 + self.x0 #DONE
        self.x_labelText           = 0.5 + self.x0 #DONE
        self.x_structLine          = 1.5 + self.x_refnum #DONE
        self.x_figure              = self.excess + self.x_structLine #DONE
        self.x_num                 = self.x_figure #DONE
        self.x_km                  = self.x_figure + np.absolute(self.minDist) #DONE
        
        
        self.x0_labelBox           = self.x_labelText - 1.5
        self.x1_labelBox           = self.x_labelText + 1.5
        self.y0_labelBox           = self.y_distUnderline
        self.y1_labelBox           = self.y_heightUnderline
        self.y2_labelBox           = self.y_figure
        self.x_boxRight            = self.x_structLine + self.structLineLength
        
        self.x1                    = self.x_structLine + self.structLineLength + 15
    
    
    def groundLine (self, f):
        """Generates the surface points of the cross-section"""
        
        
        distance = utils.format_float_array(self.section.distance[self.indexList] - self.minDist + self.x_figure);
        height   = utils.format_float_array(self.y_figure + (self.section.adjustedHeight[self.indexList] - self.h0));
        content = np.array([d + "," + h for d, h in zip(distance, height[:, 0])])[:, None]
        f.write("PLINE\n")
        np.savetxt(f, content ,fmt='%s')
        f.write("\n")
    
    
    def heightLine (self, f):
        """Generates the set of lines from the base-line to the surface"""
        
        distance = utils.format_float_array(self.section.distance[self.indexList] - self.minDist + self.x_figure);
        height   = utils.format_float_array(self.y_figure + (self.section.adjustedHeight[self.indexList] - self.h0));        
        content = np.array([
            "LINE " + d + "," + f'{utils.formatFloat(self.y_figure)} ' + d + "," + h + "\n"
            for d, h in zip(distance, height[:,0])])[:, None]
        np.savetxt(self.f, content ,fmt='%s')
        
 
 
    def axisLines (self,f):
        """Generates X and Y axis lines, baseline, and Z-axis line """
        
        x1 = utils.formatFloatArray( np.array([
            self.x_structLine,
            self.x_structLine,
            self.x_structLine,
            self.x_figure + np.absolute(self.minDist),
            self.x0_labelBox,
            self.x0_labelBox,
            self.x1_labelBox,
            self.x0_labelBox,
            self.x0_labelBox,
            self.x_boxRight
        ]))
        
        y1 = utils.formatFloatArray(np.array([
            self.y_distUnderline,
            self.y_heightUnderline,
            self.y_figure,
            self.y_figure,
            self.y0_labelBox,
            self.y0_labelBox,
            self.y0_labelBox,
            self.y2_labelBox,
            self.y1_labelBox,
            self.y_distUnderline
        ]))
        
        x2 = utils.formatFloatArray(np.array([
            self.x_structLine + self.structLineLength,
            self.x_structLine + self.structLineLength,
            self.x_structLine + self.structLineLength,
            self.x_figure + np.absolute(self.minDist),
            self.x1_labelBox,
            self.x0_labelBox,
            self.x1_labelBox,
            self.x1_labelBox,
            self.x1_labelBox,
            self.x_boxRight,
        ]))
        
        y2 = utils.formatFloatArray(np.array([
            self.y_distUnderline,
            self.y_heightUnderline,
            self.y_figure,
            self.y_figure + (self.maxHeight - self.h0) + 1,
            self.y0_labelBox,
            self.y2_labelBox,
            self.y2_labelBox,
            self.y2_labelBox,
            self.y1_labelBox,
            self.y_figure,
        ]))
        
        content = np.array([
            "LINE " + a + "," +  b + " " + c + "," + d + "\n"
            for a, b, c, d in zip(x1, y1, x2, y2)])[:, None]
        np.savetxt(self.f, content ,fmt='%s')
    
    
    def distNum (self,f):
        """Generates the distance numbers on the X-axis"""
        
        distance = utils.format_float_array(self.section.distance[self.indexList] - self.minDist + self.x_figure);
        labels   = utils.format_float_array(self.section.distance[self.indexList])
        content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_distNum) + " 0.50 90 " + l
            for d,l in zip(distance, labels)])
        np.savetxt(self.f, content ,fmt='%s')
        
    
    def heightNum (self,f):
        """Generates the height numbers on the X-axis"""
        
        distance = utils.format_float_array(self.section.distance[self.indexList] - self.minDist + self.x_figure);
        labels   = utils.format_float_array(self.section.adjustedHeight[self.indexList])[:,0]
        content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_heightNum) + " 0.50 90 " + l
            for d,l in zip(distance, labels)])
        np.savetxt(self.f, content ,fmt='%s')
        
    
    def heightRef (self,f):
        """Generates the """
        
        x = utils.formatFloat(self.x_refnum)
        y = utils.formatFloat(self.y_refnum)
        d = utils.formatFloat(self.h0)
        self.f.write(f'-TEXT M {x},{y} 0.45 0 Ref: {d}\n')
        
    
    def kmLabel (self,f):
        
        x = utils.formatFloat(self.x_km)
        y = utils.formatFloat(self.y_km)
        self.f.write(f'-TEXT M {x},{y} 0.85 0 DM: {self.section.id}\n')
        
    
    def distLabel (self,f) :
        
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_distNum)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 DIST.\n')
        
    
    def heightLabel (self, f) :
        
        x = utils.formatFloat(self.x_labelText)
        y = utils.formatFloat(self.y_heightNum)
        self.f.write(f'-TEXT M {x},{y} 0.70 90 COTA\n')
        
    
    
    def write (self):
     
        self.f.write("-LAYER N LINEA_TIERRA C 4 LINEA_TIERRA S LINEA_TIERRA L CONTINUOUS\n\n\n")
        self.groundLine(self.f)
        
        self.f.write("-LAYER N L_VERTICAL_PTO C 8 L_VERTICAL_PTO S L_VERTICAL_PTO L CONTINUOUS\n\n\n")
        self.heightLine(self.f)
        
        self.f.write("-LAYER N CAJA C 1 CAJA S CAJA L CONTINUOUS\n\n\n")
        self.axisLines(self.f)
        
        self.f.write("-LAYER N DISTANCIAS C 1 DISTANCIAS S DISTANCIAS L CONTINUOUS\n\n\n")
        self.distNum(self.f)
     
        self.f.write("-LAYER N COTAS C 3 COTAS S COTAS L CONTINUOUS\n\n\n")
        self.heightNum(self.f)
     
        self.f.write("-LAYER N REFERENCIAS C 7 REFERENCIAS S REFERENCIAS L CONTINUOUS\n\n\n")
        self.heightRef(self.f)
        self.kmLabel(self.f)
        self.distLabel(self.f)
        self.heightLabel(self.f)
        
        return self.x1



class Stack:
    
    def __init__(self, model, y):
        
        self.x0 = 0;
        self.y0 = y;
        self.currX = self.x0
        self.km0 = ""
        self.km1 = ""
        self.model = model
    
    
    def write (self, f, i , j):
        
        if i >= self.model.size:
            
            return ""
         
        
        
        
        self.km0 = self.model.getSection(i).id;
        
        iterator = mdl.ModelIterator(self.model,i,j)
        
        self.currX += 85;
        
        for section in iterator:
            
            stackElement = StackElement(section, f, x=self.currX, y=self.y0)
            self.km1 = section.id
            self.currX = stackElement.write()
            
        
        f.write("-LAYER N ENCABEZADO C 7 ENCABEZADO S ENCABEZADO L CONTINUOUS\n\n\n")
        f.write(f'-TEXT ML {self.x0},{self.y0+4} 2.50 0 PT Desde M: {self.km0}\n')
        f.write(f'-TEXT ML {self.x0},{self.y0} 2.50 0     Hasta M: {self.km1}\n')
        
        self.y0 -= 80;
        
        return self.y0




class CadScript:
    
    def __init__ (self, model):
        
        self.model = model;
        
    
    def write (self, i , j , stackSize=5.0, filename="test.txt"):
        
        y0 = 0.0
        
        with open(filename, "w") as f:
            
            while True:
                
                if  i + stackSize - 1 < j :
                    
                    stack = Stack(self.model, y0)
                    y0 = stack.write(f, i, i + stackSize - 1)
                    i += stackSize;
                    
                else:
                    
                    stack = Stack(self.model, y0)
                    stack.write(f, i, j)
                    break
    
    
    def writeKm (self,km0="0",km1="0", stackSize=5, fn="testcadkm.SCR"):
        
        i,j = self.model.getKmRange(km0,km1)
        self.write(i,j, stackSize, fn)
        
    
    def writeFull (self, path, project_name, fileSize = 100, stackSize = 5):
        
        N = self.model.size
        directory = os.path.join(path,project_name)
        os.makedirs(directory, exist_ok=True)
        
        print("Generando Scripts de CAD")
        for k in range(0,N,fileSize):
            
            if k < N:
                km = self.model.getSection(k).km
                
                file_path = os.path.join(directory, f"{project_name}-{km}.scr")
                print("Archivo: ", file_path)
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
        self.write (0, N , stackSize=stackSize, filename=filename)

