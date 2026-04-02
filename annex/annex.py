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

def trans (model,filename="annex_trans.xlsx") :
    
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet("PERFILES")
    writer = annexUtils.Writer(workbook,worksheet)
    worksheet.hide_gridlines(2)  # 2 hides both the printed and visible gridlines
    worksheet.set_portrait()
    worksheet.set_page_view(2)
    worksheet.set_paper(5)
    
    format_bold = workbook.add_format({'bold': True})
    format_border = workbook.add_format({'border': 1})
    border_top    = workbook.add_format({'top': 1})
    border_bottom = workbook.add_format({'bottom': 1})
    border_left   = workbook.add_format({'left': 1})
    border_right  = workbook.add_format({'right': 1})
    border_top_left_right = workbook.add_format({'top':1,'left':1,'right':1})

    writer.merge('B2:D6', '', {'border':1})
    writer.merge('E2:I2', '', {'right':1,'top':1,'left':1})
    writer.merge('E3:I3', 'PERFILES TRANSVERSALES', {'right':1,'left':1,'bold':True,'font_size':12,'align':'center'})
    writer.merge('E4:I5', '', {'right':1,'left':1,'bold':True,'font_size':12})
    writer.merge('E6:I6', 'FORMULARIO N° 2.5.2', {'left':1,'bottom':1,'right':1,'bold':True,'font_size':12,'align':'center'})
    
    writer.write('B8', 'PROYECTO:', {'left':1,'top':1,'bold':True,'font_size':10})
    writer.write('B9', 'SECTOR:', {'left':1,'bold':True,'font_size':10})
    writer.write('B10', 'TRAMO:', {'left':1,'bold':True,'font_size':10})
    writer.write('B12', 'REALIZADO:', {'left':1,'bottom':1,'bold':True,'font_size':10})

    writer.merge('C8:I8', '', {'right':1,'top':1,'font_size':10,'align':'left'})
    writer.merge('C9:I9', '', {'right':1,'font_size':10,'align':'left'})
    writer.merge('C10:I10', '', {'right':1,'font_size':10,'align':'left'})
    writer.merge('B11:I11', '', {'right':1,'left':1})
    writer.write('J2','',{'left':1})
    writer.merge('C12:G12', 'TOPOGRAFIA', {'bottom':1,'font_size':10,'align':'left'})
    writer.merge('H12:I12', f'FECHA: {annexUtils.curr_date()}', {'right':1,'bottom':1,'align':'right','font_size':10})

    writer.write('D14','DM',{'border':1,'font_size':10,'align':'center'})
    writer.write('E14','DIST_EJE',{'border':1,'font_size':10,'align':'center'})
    writer.write('F14','COTA',{'border':1,'font_size':10,'align':'center'})
    writer.write('G14','IDENTIFICADOR',{'border':1,'font_size':10,'align':'center'})
    
    worksheet.set_column(0,0,1) # A
    worksheet.set_column(1,1,9) # B
    worksheet.set_column(2,2,2) # C
    worksheet.set_column(3,3,14) # D
    worksheet.set_column(4,4,11) # E
    worksheet.set_column(5,5,11) # F
    worksheet.set_column(6,6,15) # G
    worksheet.set_column(7,7,9) # H
    worksheet.set_column(8,8,8) # I
    worksheet.set_column(9,9,1) # J
    
    worksheet.set_row(0,10)
    worksheet.set_row(4,8)
    worksheet.set_row(3,16)
    worksheet.set_row(6,5)
    worksheet.set_row(10,3)
    
    worksheet.set_row(7,14)
    worksheet.set_row(8,14)
    worksheet.set_row(9,14)
    
    
    
    
    END = model.get_size() + 1
    sections = mdl.ModelIterator(model,0,END+1)
    ROW = 15
    for section in sections:
        
        ascendingIndex = np.argsort(section.distance[1:])
        section.distance[1:] = section.distance[1:][ascendingIndex]
        
        descendingIndex = np.argsort(np.where(section.distance[1:]<0)[0])[::-1]
        
        # Index of the last negative number 
        neg = len(descendingIndex)
        
        # reversed ordered on negative part of distance
        section.distance[1:neg+1] = section.distance[1:][descendingIndex]
        
        section.adjustedHeight[1:] = section.adjustedHeight[1:][ascendingIndex]
        section.adjustedHeight[1:neg+1] = section.adjustedHeight[1:][descendingIndex]
        
        section.labels[1:] = section.labels[1:][ascendingIndex]
        section.labels[1:neg+1] = section.labels[1:][descendingIndex]
        
        
        pattern = r"(-[iIdD])$"
        
        # Use re.sub() to remove the suffix
        clean_labels = [re.sub(pattern, "", s) for s in section.labels]
        
        content = np.hstack((
            
            utils.round(section.matrix[:,[0]]),
            utils.round(section.distance[:,None]),
            utils.round(section.adjustedHeight)))
        
        
        for idx , row in enumerate(content):
            
            if not np.isnan(row[0]):
                writer.write(f'D{ROW}',row[0],{'left':1,'right':1,'font_size':10,'align':'center','num_format': '#,##0.000'})
                writer.write(f'G{ROW}',row[0],{'left':1,'right':1,'font_size':10,'align':'center','num_format': '#,##0.000'})
            
            else:
                writer.write(f'D{ROW}','',{'left':1,'right':1,'font_size':10,'align':'center'})
                writer.write(f'G{ROW}', clean_labels[idx],{'left':1,'right':1,'font_size':10,'align':'center'})
            
            writer.write(f'E{ROW}',row[1],{'left':1,'right':1,'font_size':10,'align':'center','num_format': '#,##0.000'})
            writer.write(f'F{ROW}',row[2],{'left':1,'right':1,'font_size':10,'align':'center','num_format': '#,##0.000'})
            
            ROW += 1
            
    writer.merge(f'D{ROW}:G{ROW}', '', Format.BTOP)
    workbook.close()

if __name__ == "__main__":
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    
    reader = rd.Reader (f1, "", f2)
    matrix, labels, om, ol, heights = reader.getData()
    model = mdl.Model(heights,matrix,labels, om, ol)
    
    
    trans (model)
    

