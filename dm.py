import xlsxwriter
import numpy as np
from collections import Counter

import xlsxwriter
import utils

from annexUtils import Format 
from annexUtils import Writer
from annexUtils import Formatter
import annexUtils

def strToFltKey (string) :
    try:
        return float(string)
    except:
        return -1

class DM :
    
    def __init__ (self,filename):
        self.dm_set = self.__init_data__(filename)
    
    def __init_data__ (self,filename) :
        if filename == "":
            return set()
        data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=0 , invalid_raise=False, usecols=(0))
        dm_idx = np.where(data != "")[0]
        return set(data[dm_idx])
    
    def get_dm_set (self):
        return self.dm_set
    
    def contains (self, dm):
        return (dm in self.dm_set)

class TransDMs :
    
    def __init__ (self,filename):
        self.dm_set = self.__init_data__(filename)
    
    def __init_data__ (self,filename) :
        if filename == "":
            return set()
        data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=0 , invalid_raise=False, usecols=(0))
        dm_idx = np.where(data != "")[0]
        return set(data[dm_idx])
    
    def get_dm_set (self):
        return self.dm_set
    
    def contains (self, dm):
        return (dm in self.dm_set)
    




class LibretaDM :
    def __init__ (self, filename) :
        self.dm_set = self.__init_data__(filename)
    
    def __init_data__ (self, filename):
        if filename =="" :
            return set()
        data = np.genfromtxt(filename, delimiter=',', dtype=str, skip_header=0 , invalid_raise=False, usecols=(1,4))
        dm_idx = np.where(data[:,1] != "")[0]
        dm_multiset = Counter(data[:,0][dm_idx])
        dm_list = [item for item, count in dm_multiset.items() if count > 1]
        return set(dm_list)
    
    def get_dm_set (self):
        return self.dm_set
    
    def contains (self, dm):
        return (dm in self.dm_set)
    


def process_dm (
        f1="",   #Archivo de "EJE ESTACA"
        f2="",   #Archivo de Perfiles transversales con coordenadas
        f3="",   #Archivo de Perfiles Transversales con descriptor
        f4="",   #Archivo de Libreta
        f5="",   #Archivo de Parche Trigonometrico
        filename = ""
):
    
    master_set  = DM (f1) 
    
    trans_coor_set = DM (f2)
    trans_desc_set = DM (f3)
    
    libreta_set = LibretaDM (f4)
    trig_set    = DM (f5)
    
    
    total_dm_set   = libreta_set.get_dm_set() | master_set.get_dm_set() | trig_set.get_dm_set()
    total_dm_list  = sorted(list(total_dm_set), key=lambda s : strToFltKey(utils.normalize_fstring(s)))
    
    
    workbook = xlsxwriter.Workbook(filename)
    ws_analisis = workbook.add_worksheet("Analisis")
    writer = Writer(workbook,ws_analisis)
    
    master_dm_true = []
    master_dm_false = []
    trans_dm_true = []
    trans_dm_false = []
    z_dm_true = []
    z_dm_false = []
    
    COL_WIDTHS = [
        1, #A 
        1.6, #B
        1.2, #C
        1.2, #D
        0.8, #E
        0.8, #F
    ]
    
    #worksheet.autofit()
    annexUtils.set_column(ws_analisis,COL_WIDTHS)
    
    writer.write("A1","DM",Format.BORDER,Format.CENTER,Format.BOLD,{'bg_color':'#dddddd'})
    writer.write("B1","Puntos Estacados",Format.BORDER,Format.CENTER,Format.BOLD,{'bg_color': '#fff196'})
    writer.write("C1","Trans Coor",Format.BORDER,Format.CENTER,Format.BOLD,{'bg_color':'#66e6e0'})
    writer.write("D1","Trans Desc",Format.BORDER,Format.CENTER,Format.BOLD,{'bg_color':'#66e6e0'})
    writer.write("E1","Libreta",Format.BORDER,Format.CENTER,Format.BOLD,{'bg_color':'#ffac73'})
    writer.write("F1","Trig",Format.BORDER,Format.CENTER,Format.BOLD,{'bg_color':'#ffac73'})
    
    ROW = 2
    
    for dm in total_dm_list:
        
        writer.write(f'A{ROW}',dm,Format.NUM,{'bg_color':'#dddddd'},Format.BORDER)
        
        # MASTER DM
        B0 =  dm in master_set.get_dm_set()
        master_dm_true.append(dm) if B0 else master_dm_false.append(dm)
        color0 = Format.COLOR_GREEN if B0 else Format.COLOR_RED
        writer.write(f"B{ROW}","",Format.BBOTTOM,Format.BTOP, {"left":2},color0)
        
        # COORDINATE TRANS  / DESCRIPTOR TRANS
        X1 = dm in trans_coor_set.get_dm_set()
        X2 = dm in trans_desc_set.get_dm_set()
        trans_dm_true.append(dm) if (X1 or X2) else trans_dm_false.append(dm)
        color1 = Format.COLOR_RED if not (X1 or X2) else ({} if not X1 else Format.COLOR_GREEN)
        color2 = Format.COLOR_RED if not (X1 or X2) else ({} if not X2 else Format.COLOR_GREEN)
        writer.write(f"C{ROW}","",Format.BBOTTOM,Format.BTOP, color1, {"left":2})
        writer.write(f"D{ROW}","",Format.BBOTTOM,Format.BTOP, color2, {"right":2})
        
        # LIBRETA / TRIGONOMETRIC
        Y1 = dm in libreta_set.get_dm_set()
        Y2 = dm in trig_set.get_dm_set()
        z_dm_true.append(dm) if (Y1 or Y2) else z_dm_false.append(dm)
        color3 = Format.COLOR_RED if not (Y1 or Y2) else ({} if not Y1 else Format.COLOR_GREEN)
        color4 = Format.COLOR_RED if not (Y1 or Y2) else ({} if not Y2 else Format.COLOR_GREEN)
        writer.write(f"E{ROW}","",Format.BBOTTOM,Format.BTOP, {"left":2},color3)
        writer.write(f"F{ROW}","",Format.BBOTTOM,Format.BTOP, {"right":2},color4)
        ROW += 1
    
        
    ws2 = workbook.add_worksheet("Eje Estacado")
    writer2 = Writer(workbook,ws2)
    annexUtils.set_column(ws2,[2,2])
    writer2.write("A1", "CUBIERTO",Format.BOLD,Format.CENTER,Format.BORDER)
    writer2.write("B1", "FALTANTE",Format.BOLD,Format.CENTER,Format.BORDER)
    
    ROW = 2
    for dm in master_dm_true:
        writer2.write(f"A{ROW}", dm, Format.BORDER, Format.COLOR_GREEN)
        ROW += 1
    
    ROW = 2
    for dm in master_dm_false:
        writer2.write(f"B{ROW}", dm, Format.BORDER, Format.COLOR_RED)
        ROW += 1
    
   
    
    ws3 = workbook.add_worksheet("Perfiles Transversales")
    writer3 = Writer(workbook,ws3)
    annexUtils.set_column(ws3,[2,2])
    writer3.write("A1", "CUBIERTO",Format.BOLD,Format.CENTER,Format.BORDER)
    writer3.write("B1", "FALTANTE",Format.BOLD,Format.CENTER,Format.BORDER)
    
    ROW = 2
    for dm in trans_dm_true:
        writer3.write(f"A{ROW}", dm, Format.BORDER, Format.COLOR_GREEN)
        ROW += 1
    
    ROW = 2
    for dm in trans_dm_false:
        writer3.write(f"B{ROW}", dm, Format.BORDER, Format.COLOR_RED)
        ROW += 1
        
        
    ws4 = workbook.add_worksheet("Cotas")
    writer4 = Writer(workbook,ws4)
    annexUtils.set_column(ws4,[2,2])
    writer4.write("A1", "CUBIERTO",Format.BOLD,Format.CENTER,Format.BORDER)
    writer4.write("B1", "FALTANTE",Format.BOLD,Format.CENTER,Format.BORDER)
    
    ROW = 2
    for dm in z_dm_true:
        writer4.write(f"A{ROW}", dm, Format.BORDER, Format.COLOR_GREEN)
        ROW += 1
    
    ROW = 2
    for dm in z_dm_false:
        writer4.write(f"B{ROW}", dm, Format.BORDER, Format.COLOR_RED)
        ROW += 1
    
    workbook.close()
    


if __name__ == "__main__" :
    
    process_dm (
        f1="/home/jstvns/axis/axis/eje-estaca.csv",
        f3="/home/jstvns/axis/axis/dat-et.txt",
        f5="/home/jstvns/axis/axis/longitudinal.txt"
    )
    
    
