import xlsxwriter
import numpy as np
import model as mdl
import utils
import annexUtils
from annexUtils import Format
import sys
import reader as rd
import re
import annexUtils

def generate (input_file, filename="eje-estaca.xlsx") :
    
    matrix = utils.read_csv(input_file)
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet("N°2.5.0")
    writer = annexUtils.Writer(workbook,worksheet)
    worksheet.hide_gridlines(2)  # 2 hides both the printed and visible gridlines
    worksheet.set_portrait()
    worksheet.set_page_view(2)
    worksheet.set_paper(5)
 
    
    COL_WIDTHS = [
        0.10, # A 
        0.99, # B
        1.2,  # C
        1.7,  # D
        1.5,  # E
        1.2,  # F
        0.1,  # G
    ]
    
    ROW_DICT = {
        0 :0.1,   # Upper Margin
        6 :0.1,   # Interheader Margin
        10:0.08,  #
        12:0.12,
    }
    
    #worksheet.autofit()
    annexUtils.set_column(worksheet,COL_WIDTHS)
    annexUtils.set_row_dict(worksheet,ROW_DICT)
    
    
    
    
    writer.merge(f'B1:F1', "", Format.BBOTTOM)
    writer.merge(f'A2:A6', "", Format.BRIGHT)
    writer.merge(f'G2:G6', "", Format.BLEFT)
    writer.merge(f'B7:F7', "", Format.BTOP, Format.BBOTTOM)
    
    writer.merge('B13:F13', "", Format.BTOP)
    writer.merge('A8:A12',  "", Format.BRIGHT)
    writer.merge('G8:G12',  "", Format.BLEFT)
    
    writer.merge('C2:C6',  "", Format.BRIGHT)
    
    writer.merge('D3:F3', 'COORDENADAS DE PUNTOS ESTACADOS', Format.CENTER, Format.SIZE(12), Format.BOLD)
    writer.merge('D6:F6', 'FORMULARIO N°2.5.0', Format.CENTER, Format.SIZE(12), Format.BOLD)
    
    writer.write('B8',  'PROYECTO', Format.BOLD, Format.SIZE(10))
    writer.write('B9',  'SECTOR', Format.BOLD, Format.SIZE(10))
    writer.write('B10', 'TRAMO', Format.BOLD, Format.SIZE(10))
    writer.write('B12', 'REALIZADO', Format.BOLD, Format.SIZE(10))
    writer.merge('E12:F12', f'FECHA: {annexUtils.curr_date()}', Format.RIGHT, Format.SIZE(10))
    
    writer.write('B14', 'N°', Format.BORDER)
    writer.write('C14', 'DM', Format.BORDER)
    writer.write('D14', 'NORTE', Format.BORDER)
    writer.write('E14', 'ESTE', Format.BORDER)
    writer.write('F14', 'DESCRIPCIÓN', Format.BORDER)
    
    curr_row = 15
    curr_point = 0
    for row in matrix:
        writer.write(f'B{curr_row}', curr_point, Format.BORDER)
        writer.write(f'C{curr_row}', float(row[0]), Format.BORDER, Format.NUM)
        writer.write(f'D{curr_row}', float(row[1]), Format.BORDER, Format.NUM)
        writer.write(f'E{curr_row}', float(row[2]), Format.BORDER, Format.NUM)
        try:
            writer.write(f'F{curr_row}', row[3], Format.BORDER)
        except IndexError :
            print("Error al escribir descriptor")
        curr_row += 1
        curr_point += 1
    
    
    
    
    
    workbook.close()

if __name__ == "__main__":
    
    generate("/home/jstvns/eje-estaca.csv")
    
