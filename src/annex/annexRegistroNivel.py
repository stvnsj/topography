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
    
    workbook   = xlsxwriter.Workbook(output_file)
    worksheet  = workbook.add_worksheet("Registro Nivelación Geom.")
    
    worksheet.hide_gridlines(2)
    worksheet.set_portrait()
    worksheet.set_page_view(2)
    worksheet.set_paper(9)
    worksheet.set_margins(left=0.71, right=0.71, top=0.95, bottom=0.75)
    
    writer = Writer(workbook,worksheet)
    
    # FIXED CONTENT
    writer.merge(f"B2:C6","",Format.BORDER)
    
    writer.merge(
        f"D2:H5","REGISTRO DE NIVELACIÓN GEOMÉTRICA",
        Format.BTOP,Format.BRIGHT,Format.SIZE(12),Format.BOLD,
        Format.CENTER, Format.VCENTER
    )
    
    writer.merge(
        f"D6:H6",
        "TABLA 2.305.301.A",
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
    

    writer.merge("C15:E15", "LECTURAS EN LA MIRA" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.merge("F15:G15", "COTAS" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)

    writer.merge("B15:B16", "PUNTOS" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.write("C16", "ATRAS" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.write("D16", "INTERM." , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.write("E16", "ADELANTE" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.write("F16", "INSTRM." , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.write("G16", "DEL PUNTO" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
    writer.merge("H15:H16", "OBSERVACIONES" , Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)

    
    curr_row = 17
    
    COL_WIDTH = [
        0.1, # A
        0.99, # B
        0.90, # C ATRAS
        0.90, # D INTERM
        0.90, # E ADELANTE
        0.99, # F
        0.99, # G
        (1.50), # H
        0.1, # I   
    ]
    
    annexUtils.set_column(worksheet,COL_WIDTH)


    for segment in cir.negative:
        curr_row += 1
        TABLE = segment.get_registro_nivelacion ()
        for ROW in TABLE:
            PUNTO = ROW[0]
            ATRAS = utils.normalize_fstring (ROW[1])
            INTER = utils.normalize_fstring(ROW[2])
            ADELANTE  = utils.normalize_fstring(ROW[3])
            CORR_INSTR = utils.normalize_fstring(ROW[4])
            CORR_PUNTO = utils.normalize_fstring(ROW[5])

            writer.write(f'B{curr_row}', PUNTO,      Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
            writer.write(f'C{curr_row}', ATRAS,      Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER,Format.NUM)
            writer.write(f'D{curr_row}', INTER,      Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER,Format.NUM)
            writer.write(f'E{curr_row}', ADELANTE,   Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER,Format.NUM)
            writer.write(f'F{curr_row}', CORR_INSTR, Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER,Format.NUM)
            writer.write(f'G{curr_row}', CORR_PUNTO, Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER,Format.NUM)
            writer.write(f'H{curr_row}', "", Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)

  
            curr_row += 1

    curr_row += 1
    for segment in cir.positive:
        TABLE = segment.get_registro_nivelacion ()
        for ROW in TABLE:
            PUNTO = ROW[0]
            ATRAS = ROW[1]
            INTER = ROW[2]
            ADELANTE  = ROW[3]
            CORR_INSTR = ROW[4]
            CORR_PUNTO = ROW[5]

            writer.write(f'B{curr_row}', PUNTO,      Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
            writer.write(f'C{curr_row}', ATRAS,      Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER, Format.NUM)
            writer.write(f'D{curr_row}', INTER,      Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER, Format.NUM)
            writer.write(f'E{curr_row}', ADELANTE,   Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER, Format.NUM)
            writer.write(f'F{curr_row}', CORR_INSTR, Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER, Format.NUM)
            writer.write(f'G{curr_row}', CORR_PUNTO, Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER, Format.NUM)
            writer.write(f'H{curr_row}', "", Format.CENTER, Format.SIZE(10), Format.BORDER, Format.VCENTER)
  
            curr_row += 1

    

    
    writer.merge(f'C{curr_row}:G{curr_row}', '', Format.BTOP)
    annexUtils.set_row_dict(worksheet,ROW_DICT)
    
    workbook.close()
    



if __name__ == "__main__":
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    generate(f1, f2)
