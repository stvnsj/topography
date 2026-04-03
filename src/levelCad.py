import utils
import numpy as np


class LevelCad :
    
    def __init__ (self,data):
        
        self.data = data
        
        
        self.x0 = 0.0
        self.y0 = 0.0
        
        self.min_dm = data[0][0]
        self.max_dm = data[-1][0]
        
        self.range_dm = utils.round(self.max_dm - self.min_dm)
        self.excess = 2.0
        
        self.structLineLength = self.range_dm + 2 * self.excess
        
        self.minHeith = np.min(data[:,1])
        
        self.h0 = int(self.minHeith) - 2
        
        self.y_km              = self.y0
        self.y_distUnderline   = 0.5 + self.y_km
        self.y_distNum         = 2.1 + self.y_distUnderline
        self.y_heightUnderline = 2.1 + self.y_distNum
        self.y_heightNum       = 2.1 + self.y_heightUnderline
        self.y_figure          = 2.1 + self.y_heightNum
        self.y_refnum          = 0.5 + self.y_figure
        
        self.x_refnum          = 0.5 + self.x0
        self.x_labelText       = 0.5 + self.x0
        self.x_structLine      = 1.5 + self.x_refnum
        self.x_figure          = self.excess + self.x_structLine
        self.x_num             = self.x_figure
        
        self.x0_labelBox       = self.x_labelText - 1.5
        self.x1_labelBox       = self.x_labelText + 1.5
        self.y0_labelBox       = self.y_distUnderline
        self.y1_labelBox       = self.y_heightUnderline
        self.y2_labelBox       = self.y_figure
        self.x_boxRight        = self.x_structLine + self.structLineLength
    
    
    def write(self,f):
        
        
        distance = utils.format_float_array( self.data[:,0] - self.min_dm + self.x_figure )
        height   = utils.format_float_array( self.data[:,1] - self.h0 + self.y_figure )
        
        height_scaled = utils.format_float_array( 10.0 * (self.data[:,1] - self.h0) + self.y_figure )
        
        
        ground = np.array(
            [d + "," + h for d, h in zip(distance, height_scaled)])[:, None]
        
        vertical = np.array([
            "LINE " + d + "," + f'{utils.formatFloat(self.y_figure)} ' + d + "," + h + "\n"
            for d, h in zip(distance, height_scaled)])[:, None]
        
        x1 = utils.formatFloatArray( np.array([
            self.x_structLine,
            self.x_structLine,
            self.x_structLine,
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
            self.y0_labelBox,
            self.y2_labelBox,
            self.y2_labelBox,
            self.y2_labelBox,
            self.y1_labelBox,
            self.y_figure,
        ]))
        
        box = np.array([
            "LINE " + a + "," +  b + " " + c + "," + d + "\n"
            for a, b, c, d in zip(x1, y1, x2, y2)])[:, None]
        
        dm_index = [i for i in range(0,len(self.data[:,0]),10)]
        dm_content = np.array([
            "-TEXT M " + d + "," + f'{self.y_km} 0.50 0 ' + utils.format_float(l)
            for d , l in zip (distance[dm_index] , self.data[:,0][dm_index])
        ])
        
        dm_label   = utils.format_float_array(self.data[:,0])
        dm_label_content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_distNum) + " 0.50 90 " + l
            for d,l in zip(distance, dm_label)])
        
        h_label    = utils.format_float_array(self.data[:,1])
        h_label_content = np.array([
            "-TEXT M " + d + "," + utils.formatFloat(self.y_heightNum) + " 0.50 90 " + l
            for d,l in zip(distance, h_label)])
        
        
        f.write("-LAYER N LINEA_TIERRA C 4 LINEA_TIERRA S LINEA_TIERRA L CONTINUOUS\n\n\n")
        f.write("PLINE\n")
        np.savetxt(f, ground ,fmt='%s')
        f.write("\n")
        
        f.write("-LAYER N L_VERTICAL_PTO C 8 L_VERTICAL_PTO S L_VERTICAL_PTO L CONTINUOUS\n\n\n")
        np.savetxt(f, vertical ,fmt='%s')
        
        f.write("-LAYER N CAJA C 1 CAJA S CAJA L CONTINUOUS\n\n\n")
        np.savetxt(f, box ,fmt='%s')
        
        f.write("-LAYER N DISTANCIAS C 1 DISTANCIAS S DISTANCIAS L CONTINUOUS\n\n\n")
        np.savetxt(f, dm_label_content ,fmt='%s')
     
        f.write("-LAYER N COTAS C 3 COTAS S COTAS L CONTINUOUS\n\n\n")
        np.savetxt(f, h_label_content ,fmt='%s')
        
        f.write("-LAYER N REFERENCIAS C 7 REFERENCIAS S REFERENCIAS L CONTINUOUS\n\n\n")
        np.savetxt(f, dm_content, fmt='%s')
        f.write(f'-TEXT M {utils.formatFloat(self.x_refnum)},{utils.formatFloat(self.y_refnum)} 0.45 0 Ref: {utils.formatFloat(self.h0)}\n')
        f.write(f'-TEXT M {utils.formatFloat(self.x_labelText)},{utils.formatFloat(self.y_distNum)} 0.70 90 DM\n')
        f.write(f'-TEXT M {utils.formatFloat(self.x_labelText)},{utils.formatFloat(self.y_heightNum)} 0.70 90 COTA\n') 
