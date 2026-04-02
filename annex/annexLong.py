import xlsxwriter
import openpyxl
import numpy as np
import model as mdl
import utils
import sys
import reader as rd
import re
import annexUtils
from annexUtils import Format 
from annexUtils import Writer
from annexUtils import Formatter
from openpyxl   import load_workbook
import level

ROW_DICT = {
    0:0.1,
    6:0.1,
    10:0.1,
    12:0.1,13:0.1
}

def generate (
        input1 = "",
        input2 = "",
        input3 = "",
        output_file = "testlongi.xlsx") :
    
    cir = level.parser(input1, input2, input3)
    TABLE = cir.get_report_long()
    
    workbook   = xlsxwriter.Workbook(output_file)
    worksheet  = workbook.add_worksheet("NIVELACION LONGITUDINAL")
    
    worksheet.hide_gridlines(2)
    worksheet.set_portrait()
    worksheet.set_page_view(2)
    worksheet.set_paper(9)
    worksheet.set_margins(left=0.71, right=0.71, top=0.95, bottom=0.75)
    
    writer = Writer(workbook,worksheet)
    
    # FIXED CONTENT
    writer.merge(f"B2:C6","",Format.BORDER)
    
    writer.merge(
        f"D2:H5","NIVELACIÓN LONGITUDINAL DEL EJE ESTACADO",
        Format.BTOP,Format.BRIGHT,Format.SIZE(12),Format.BOLD,
        Format.CENTER, Format.VCENTER
    )
    
    writer.merge(
        f"D6:H6",
        "FORMULARIO N° 2.5.3",
        Format.BBOTTOM,Format.BRIGHT,Format.SIZE(12),
        Format.BOLD,Format.CENTER
    )
    
    writer.write(f"I2","",Format.BLEFT)
    writer.merge(f"B7:H7","",{"bottom":1})
    writer.merge(f"A8:A12","",{"right":1})
    writer.merge(f"I8:I12","",{"left":1})
    writer.merge(f"B13:H13","",{"top":1})
    
    writer.write(f"B8","PROYECTO",Format.SIZE(10), Format.BOLD, Format.LEFT, Format.VCENTER)
    writer.write(f"B9","SECTOR", Format.SIZE(10),Format.BOLD, Format.LEFT, Format.VCENTER)
    writer.write(f"B10","TRAMO", Format.SIZE(10),Format.BOLD, Format.LEFT, Format.VCENTER)
    writer.write(f"B12","REALIZADO",Format.SIZE(10), Format.BOLD, Format.LEFT, Format.VCENTER)
    writer.merge(f"G12:H12",f"FECHA: {annexUtils.curr_date()}",Format.SIZE(10),Format.RIGHT,Format.VCENTER)
    
    writer.write("C15", "DM" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.write("D15", "IDA" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.write("E15", "VUELTA" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.write("F15", "DIFERENCIA" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.write("G15", "PROMEDIO" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    
    curr_row = 16
    
    COL_WIDTH = [
        0.1, # A
        0.99, # B
        0.99, # C
        0.99, # D
        0.99, # E
        0.99, # F
        0.99, # G
        0.99, # H
        0.1, # I   
    ]
    
    annexUtils.set_column(worksheet,COL_WIDTH)
    
    for ROW in TABLE:
        V_DM = ROW[0]
        V_IDA = ROW[1]
        V_VUELTA = ROW[2]
        V_DIF  = ROW[3]
        V_MEAN = ROW[4]
        V_TRIG = ROW[5]
        
        writer.write(f'C{curr_row}', V_DM,     Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER, Format.NUM)
        writer.write(f'D{curr_row}', V_IDA,    Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER, Format.NUM)
        writer.write(f'E{curr_row}', V_VUELTA, Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER, Format.NUM)
        writer.write(f'F{curr_row}', V_DIF,    Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER, Format.NUM)
        writer.write(f'G{curr_row}', V_MEAN,   Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER, Format.NUM)
        if V_TRIG > 0:
            writer.write(f'H{curr_row}', "* COTA TRIG", Format.CENTER, Format.ITALIC, Format.SIZE(9))
        
        
        curr_row += 1
    
    writer.merge(f'C{curr_row}:G{curr_row}', '', Format.BTOP)
    annexUtils.set_row_dict(worksheet,ROW_DICT)
    
    workbook.close()
    



if __name__ == "__main__":
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    generate(f1, f2)
