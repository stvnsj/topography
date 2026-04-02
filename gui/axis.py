################
# AXIS IMPORTS #
################
import model as md
from . import action as ax_com
from .rootFrame import root
from . import component
from .stringvar import *


####################
# EXTERNAL IMPORTS #
####################
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage,Label
import numpy as np
from tkinter import ttk
from tkinter.ttk import Style
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from tkinter.filedialog import asksaveasfile
import sys

trans_model = None


# Create main window

root.title("Sistema de Procesamiento Topográfico")
root.geometry("1200x950")


# Create a Notebook widget (tabs container)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

#s = Style()
#s.configure('My.TFrame', background='#111111')


# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab6 = ttk.Frame(notebook)
tab7 = ttk.Frame(notebook)
tab8 = ttk.Frame(notebook)



# Add tabs to the notebook (tabs container)
notebook.add(tab1, text='CAD')
notebook.add(tab2, text='NIVELACION')
notebook.add(tab3, text='ANEXO (Ante.)')
notebook.add(tab4, text='ANEXO (Def.)')
notebook.add(tab6, text='PLOT')
notebook.add(tab7, text='CONTROL')
notebook.add(tab8, text='HERRAMIENTAS')




descriptor_file_param = {"label": "Estacado con Descriptor", "stringvar": descriptor_file, "type":"file" , "field": 'estacado-descriptor'}
coordinate_file_param = {"label": "Estacado con Coordenadas", "stringvar": coordinate_file , "type":"file", 'field': "estacado-coordenadas"}
longitudinal_file_param = {"label": "Longitudinal", "stringvar": longitudinal_file , "type":"file", 'field': 'longitudinal'}
pr_height_file_param = {"label": "Cotas Topograficas", "stringvar": pr_height_file , "type":"file", 'field':'cotas-pr'}
libreta_file_param = {"label": "Circuito Nivelación", "stringvar": libreta_file , "type":"file", 'field':'libreta'}
trigonometric_file_param = {"label": "Alturas Trigonométricas", "stringvar": trigonometric_file, "type":"file", 'field':'trigonometrica'}
master_table_file_param = {"label":"Anexo 1 (Tabla Maestra)", "stringvar": master_table_file ,  "type":"file", "field":"anexo-1"}
master_pr_file_param = {"label":"Tabla Maestra PR", "stringvar": master_pr_file ,  "type":"file", "field":"master-pr"}
pr_level_file_param = {"label":"Anexo 10 (Nivelación)"  , "stringvar": pr_level_file , "type":"file", "field":"anexo-10"}
img_dir1_param = {"label":"Imagenes (Pan. Det.)"   , "stringvar": img_dir1 , "type":"dir", "field":'fotos'}
img_dir2_param = {"label":"Imagenes (a. p. g.)"        , "stringvar": img_dir2 , "type":"dir", "field":'georef'}
eje_estaca_file_param = {"label":"Eje Estaca", "stringvar": eje_estaca_file, "type":"file", "field":'eje-estaca'}

mop_proj_file_param = {"label": "MOP Proyecto",    "stringvar": mop_proj_file , "type":"file", "field":"mop-proj"}
mop_ctrl_file_param = {"label": "MOP Autocontrol", "stringvar": mop_ctrl_file , "type":"file", "field":"mop-ctrl"}

level_proj_file_param = {"label": "Nivelación Proyecto",     "stringvar": level_proj_file, "type":"file", "field":"level-proj"}
level_ctrl_file_param = {"label": "Nivelación Autocontrol" , "stringvar": level_ctrl_file, "type":"file", "field":"level-ctrl"}

axis_proj_file_param  = {"label": "Eje Estacado de Proyecto",    "stringvar":axis_proj_file, "type":"file", "field":"axis-proj"}
axis_ctrl_file_param  = {"label": "Eje Estacado de Autocontrol", "stringvar":axis_ctrl_file, "type":"file", "field":"axis-ctrl"}

mdt_proj_file_param = {"label": "MDT Proyecto",    "stringvar":mdt_proj_file, "type":"file", "field":"mdt-proj"}
mdt_ctrl_file_param = {"label": "MDT Autocontrol", "stringvar":mdt_ctrl_file, "type":"file", "field":"mdt-ctrl"}


mop_to_ter_file_param = {
    "label": "MOP",
    "stringvar": mop_to_ter,
    "type":"file",
    "field": "mop-to-ter"
}

river_axis_file_param = {
    "label" : "Perfil de Cauce",
    "stringvar" : river_axis,
    "type" : "file",
    "field" : "river-axis"
}

libreta_app_file_param = {
    "label" : "Libreta de Aplicación",
    "stringvar" : libreta_app,
    "type" : "file",
    "field" : "libreta-app"
}





################
# ############ #
# # CAD TAB1 # #
# ############ #
################
button_params = [
    descriptor_file_param,
    coordinate_file_param,
    longitudinal_file_param
]

component.LoadFileFrame(tab1, title="Carga de Archivos", button_params = button_params)



chk = tk.Checkbutton(
    tab1,
    text="Cercos",
    variable=cerco_switch,
    onvalue=True,
    offvalue=False
)
chk.pack(padx=20, pady=10)

entry_params = [
    {"label":"Perfiles por Fila" , "var" : stackLength},
    {"label":"Escala vertical" , "var" : yscale}
]
component.InputFrame(tab1,entry_params=entry_params, command=ax_com.complete_cad, title="CAD Proyecto Completo")

entry_params = [
    {"label":"Perfiles por Fila" , "var" : stackLength},
    {"label":"Perfiles por Archivo" , "var" : chunkSize },
    {"label":"Nombre Proyecto" , "var" : projectName},
    {"label":"Escala vertical" , "var" : yscale}
]

component.InputFrame(tab1,entry_params=entry_params, command=ax_com.generateFullCAD, title="CAD Proyecto Fragmentado")

entry_params = [
    {"label":"Metros Inicio" , "var" : meter0},
    {"label":"Metros Final", "var" : meter1},
    {"label":"Perfiles por fila", "var" : stackLength},
    {"label":"Escala vertical" , "var" : yscale}
]

component.InputFrame(tab1,entry_params=entry_params, command=ax_com.generateCAD, title="CAD de Tramo")


button_params = [
    {"label":"MOP", "command":ax_com.generateMOP},
    {"label":"Coordenadas (cota ajustada)", "command":ax_com.action_coordinate_z},
    {"label":"Anchos", "command":ax_com.generateAnchos}
]
component.ButtonFrame(tab1, title="Planillas", button_params=button_params)


















################
# ############ #
# # CAD TAB8 # #
# ############ #
################

button_params = [mop_to_ter_file_param]
component.InputOutputFrame(
    tab8, 
    title="Conversión MOP → TER", 
    button_params = button_params,
    command=ax_com.mop_to_ter_action
)

button_params = [libreta_app_file_param]
component.InputOutputFrame(
    tab8, 
    title="Conversión Libreta Celular → Computador", 
    button_params = button_params,
    command=ax_com.convert_libreta_action
)

button_params = [river_axis_file_param]
component.InputOutputFrame(
    tab8,
    title="Procesamiento Perfiles de Cauce con Millón", 
    button_params = button_params,
    command=ax_com.process_river_action
)






#######################
# ################### #
# # NIVELACION TAB2 # #
# ################### #
#######################

button_params = [
    pr_height_file_param,
    libreta_file_param,
    trigonometric_file_param,
]
component.LoadFileFrame(tab2, title="Carga de Archivos", button_params = button_params)


button_params = [
    {"label":"Anexo 2.5.3 (CSV)","command":ax_com.generate_report},
    {"label":"Longitudinal", "command":ax_com.generate_longitudinal},
    {"label":"CAD" , "command":ax_com.generate_height_cad}
]
component.ButtonFrame(tab2, title="Planillas", button_params=button_params)



############################################################################
#              _   _ _   _ ________   __                                   #
#        /\   | \ | | \ | |  ____\ \ / /                                   #
#       /  \  |  \| |  \| | |__   \ V /                                    #
#      / /\ \ | . ` | . ` |  __|   > <                                     #
#     / ____ \| |\  | |\  | |____ / . \                                    #
#    /_/    \_\_| \_|_| \_|______/_/ \_\                                   #
#                                                                          #
#                                                                          #
#  _____  ______ ______ _____ _   _ _____ _______ _______      ______      #
# |  __ \|  ____|  ____|_   _| \ | |_   _|__   __|_   _\ \    / / __ \     #
# | |  | | |__  | |__    | | |  \| | | |    | |    | |  \ \  / / |  | |    #
# | |  | |  __| |  __|   | | | . ` | | |    | |    | |   \ \/ /| |  | |    #
# | |__| | |____| |     _| |_| |\  |_| |_   | |   _| |_   \  / | |__| |    #
# |_____/|______|_|    |_____|_| \_|_____|  |_|  |_____|   \/   \____/     #
############################################################################

annex250_frame = tk.Frame(tab4, padx=3, pady=3, bd=3, relief="raised")

button_params = [eje_estaca_file_param]
component.LoadFileFrame(annex250_frame, title="Carga de Archivos Eje Estaca", button_params = button_params)


button_params = [
    {"label":"Eje Estaca (3.5.0)", "command":ax_com.generate_eje_estaca},
]
component.ButtonFrame(annex250_frame,button_params=button_params)
annex250_frame.pack()


annex252_frame = tk.Frame(tab4, padx=3, pady=3, bd=3, relief="raised")

button_params = [descriptor_file_param, coordinate_file_param, longitudinal_file_param]
component.LoadFileFrame(annex252_frame, title="Carga de Archivos Estacado", button_params = button_params)


button_params = [
    {"label":"Perfiles Transversales (2.5.2)", "command":ax_com.generate_anexo_trans},
]
component.ButtonFrame(annex252_frame,button_params=button_params)
annex252_frame.pack()

annex253_frame = tk.Frame(tab4, padx=3, pady=3, bd=3, relief="raised")

button_params = [pr_height_file_param,libreta_file_param,trigonometric_file_param]
component.LoadFileFrame(annex253_frame, title="Carga de Archivos Nivelación", button_params = button_params)

button_params = [
    {"label":"Nivelación Longitudinal del Eje Estacado (2.5.3)",
     "command": ax_com.generate_annex_long},
]
component.ButtonFrame(annex253_frame,button_params=button_params)

annex253_frame.pack()




annex253_frame = tk.Frame(tab4, padx=3, pady=3, bd=3, relief="raised")

button_params = [pr_height_file_param,libreta_file_param]
component.LoadFileFrame(annex253_frame, title="Carga de Archivos Nivelación", button_params = button_params)

button_params = [
    {"label":"Registro de Nivelación Geométrica (2.305.302.A)",
     "command": ax_com.generate_annex_registro_nivelacion},
]
component.ButtonFrame(annex253_frame,button_params=button_params)

annex253_frame.pack()



########################
# ANEXO ANTEPROYECTO   #
########################
button_params = [
    master_table_file_param,
    master_pr_file_param,
    pr_level_file_param,
    #img_dir1_param,
    img_dir2_param,
]

component.LoadFileFrame(tab3, title='Carga de Anexos', button_params=button_params)


button_params = [
    {"label":"2 - Puntos de la Red de Referencia Principal (2.903.3.F)", "command":ax_com.generate_annex_2},
    {"label":"4 - Resumen de Coordenadas de la Red de Referencia Principal (2.903.3.G)", "command":ax_com.generate_annex_4},
    {"label":"5 - Formulario de Ubicación de Vértices del STC (2.303.104.A)", "command":ax_com.generate_annex_5},
    {"label":"8 - Coordenadas de Vértices del STC (2.303.104.B)", "command":ax_com.generate_annex_8},
    {"label":"9 - Monografías de PR", "command":ax_com.generate_annex_9},
    {"label":"11 - Cotas de PR (2.903.3.I)", "command":ax_com.generate_annex_11},
]
component.ButtonFrame(tab3, title="Generación de Anexos (ANTEPROYECTO)", button_params=button_params)


annex_parameters = tk.Frame(tab3,padx=3, pady=3, bd=3, relief="raised",width = 1000)
annex_parameters.pack()

annex_parameter_frame_title = tk.Label(annex_parameters, text="Parametros Anexos", font=("Arial", 14, "bold"))
annex_parameter_frame_title.pack(anchor="n")

entry_params = [
    {"label":"Zoom Imagen Detalle" ,    "var" : detail_image_zoom},
]

component.InputFrame(annex_parameters,entry_params=entry_params, button= False ,title="Parametros")



################################
#  _____  _      ____ _______  #
# |  __ \| |    / __ \__   __| #
# | |__) | |   | |  | | | |    #
# |  ___/| |   | |  | | | |    #
# | |    | |___| |__| | | |    #
# |_|    |______\____/  |_|    #
################################


fig, ax = plt.subplots(figsize=(11, 11))
# Contains the PLOT buttons and menus.
plot_frame = tk.Frame(tab6)
# Contains the combobox menu.
combobox_frame = ttk.LabelFrame(plot_frame, text="Perfil Transversal")
# Combox menu to select a cross section DM.
combobox = ttk.Combobox(combobox_frame, values=[])
# Contains the "siguiente" and "previo" buttons.
navigation_frame = ttk.LabelFrame(plot_frame, text="Navegar Perfiles")
# Plots the next cross section.
next_button = tk.Button(navigation_frame, text="siguiente", command=lambda: ax_com.next_section_index(fig,ax,canvas,plot_index))
# Plots the previous cross section
prev_button = tk.Button(navigation_frame, text="previo", command=lambda: ax_com.prev_section_index(fig,ax,canvas, plot_index))

# DM Frame.
dm_frame   = ttk.LabelFrame(plot_frame, text="DM")
dm_display = tk.Label(dm_frame, textvariable=plot_index, bg='white', bd=1, relief="solid", width=10, anchor="w")


# Contains the PLOT and the Matplotlib Navigation Bar
canvasFrame = tk.Frame(tab6,bd=5,relief='groove',bg='#BBBBBB')
# This frame contains the PLOT
canvas = FigureCanvasTkAgg(fig, master=canvasFrame)
# Contains the Navigation BAR
toolbar = NavigationToolbar2Tk(canvas, canvasFrame)

def on_combobox_select(event):
    dm = combobox.get()
    i  = ax_com.km_idx_dict.get(dm)
    ax_com.update_section_index(i)
    ax_com.plot_test(fig,ax,canvas)
    plot_index.set(dm)

combobox.bind("<<ComboboxSelected>>", on_combobox_select)
button_params = [
    descriptor_file_param,
    coordinate_file_param,
    longitudinal_file_param,
]

component.LoadFileFrame(tab6, title="Carga de Archivos", button_params = button_params)

button_params = [
    {"label":"Generar Modelo", "command":  lambda : ax_com.generate_model(descriptor_file, coordinate_file, longitudinal_file, combobox,fig, ax, canvas)},
#    {"label":"Graficar",       "command":  lambda : ax_com.plot_test(fig,ax,canvas)}
]
component.ButtonFrame(tab6, title="Generar Modelo", button_params=button_params)

combobox_frame.grid(column=0,row=0, padx=10, pady=10,)
navigation_frame.grid(column=1,row=0, padx=10, pady=10)
dm_frame.grid(column=2, row=0, padx = 10, pady=10)

# canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)


plot_frame.pack()


combobox.pack(padx = 5, pady = 5)
#canvas.get_tk_widget().pack()
prev_button.grid(column=0,row=0)
next_button.grid(column=1,row=0)
dm_display.pack()
canvas.get_tk_widget().pack(fill='both' , expand=True)
toolbar.pack()
canvasFrame.pack(fill='both',expand=True)




#         _    _ _______ ____   _____ ____  _   _ _______ _____   ____  _       
#    /\  | |  | |__   __/ __ \ / ____/ __ \| \ | |__   __|  __ \ / __ \| |      
#   /  \ | |  | |  | | | |  | | |   | |  | |  \| |  | |  | |__) | |  | | |      
#  / /\ \| |  | |  | | | |  | | |   | |  | | . ` |  | |  |  _  /| |  | | |      
# / ____ \ |__| |  | | | |__| | |___| |__| | |\  |  | |  | | \ \| |__| | |____  
#/_/    \_\____/   |_|  \____/ \_____\____/|_| \_|  |_|  |_|  \_\\____/|______| 
canvas = tk.Canvas(tab7)
canvas.pack(side = 'left', fill='both', expand=True)




scrollbar = tk.Scrollbar(tab7, orient='vertical', command=canvas.yview)
scrollbar.pack(side = 'right', fill='y')

canvas.configure(yscrollcommand=scrollbar.set)







control_frame = tk.Frame(tab7,padx=40, pady=28,width = 1100)
canvas.create_window(
    (5,0),
    window=control_frame,
    anchor='n'
)

control_parameter_frame = tk.Frame(control_frame,padx=3, pady=3, bd=3, relief="raised",width = 1000)
control_parameter_frame.pack()

control_parameter_frame_title = tk.Label(control_parameter_frame, text="Parametros Globales", font=("Arial", 14, "bold"))
control_parameter_frame_title.pack(anchor="n")

entry_params = [
    {"label":"Semilla de Aleatoriedad" ,    "var" : random_seed_input},
    {"label":"Longitud Total de Proyecto" , "var" : project_length_input},
    {"label":"Tramo"                      , "var" : dm_interval_input}
]

component.InputFrame(control_parameter_frame,entry_params=entry_params, button= False ,title="Parametros")



mop_frame = tk.Frame(control_frame,padx=3, pady=3, bd=3, relief="raised")
mop_frame.pack()

mop_frame_title = tk.Label(mop_frame, text="Autocontrol Longitudinal y Transversal", font=("Arial", 14, "bold"))
mop_frame_title.pack(anchor="n")

button_params = [
    mop_proj_file_param,
    mop_ctrl_file_param,
    level_proj_file_param,
    level_ctrl_file_param,
]
component.LoadFileFrame(mop_frame, title='Carga de Archivos', button_params=button_params)


button_params = [
    {"label":"Optimizar semilla", "command":ax_com.optimize_seed},    
    {"label":"Autocontrol Longitudinal (CSV)", "command":ax_com.generate_level_control},
    {"label":"Autocontrol Transversal Completo (CSV)", "command":ax_com.generate_mop_control_full},
    {"label":"Autocontrol Transversal Aleatorio (CSV)", "command":ax_com.generate_mop_control_random},
    {"label":"CAD de Autocontrol Transversal (SCR)", "command":ax_com.generate_mop_cad_control},
    {"label":"Autcontrol de Línea de Tierra (XLSX)", "command":ax_com.generate_groundline_control},  
]

component.ButtonFrame(mop_frame, title="Generación de Archivos", button_params=button_params)


axis_frame = tk.Frame(control_frame,padx=4, pady=20, bd=3, relief="raised")
axis_frame.pack()
axis_frame_title = tk.Label(axis_frame, text="Autocontrol de Eje Estacado", font=("Arial", 14, "bold"))
axis_frame_title.pack(anchor="n")
button_params = [
    axis_proj_file_param,
    axis_ctrl_file_param
]
component.LoadFileFrame(axis_frame, title='Carga de Archivos', button_params=button_params)

button_params = [
    {"label": "Autocontrol de Eje Estacado (CSV)", "command": ax_com.generate_axis_control_csv},
    {"label": "Autocontrol de Eje Estacado (XLSX)", "command": ax_com.generate_axis_control_annex}
]

component.ButtonFrame(axis_frame, title="Generación de Archivos", button_params=button_params)

mdt_frame = tk.Frame(control_frame,padx=3, pady=3, bd=3, relief="raised")
mdt_frame.pack()
mdt_frame_title = tk.Label(mdt_frame, text="Autocontrol de MDT", font=("Arial", 14, "bold"))
mdt_frame_title.pack(anchor="n")
button_params = [
    mdt_proj_file_param,
    mdt_ctrl_file_param,
]
component.LoadFileFrame(mdt_frame, title='Carga de Archivos', button_params=button_params)
button_params = [
    {"label": "Autocontrol de MDT (CSV)",  "command": ax_com.generate_mdt_control_csv},
    {"label": "Autocontrol de MDT (XLSX)", "command": ax_com.generate_mdt_control_annex},    
]
component.ButtonFrame(mdt_frame, title="Generación de Archivos", button_params=button_params)










def update_scroll_region(event) :
    canvas.configure(scrollregion=canvas.bbox('all'))
control_frame.bind("<Configure>", update_scroll_region)





def on_closing():
    plt.close("all")  # Close all Matplotlib figures
    root.quit()       # Quit the Tkinter main loop
    root.destroy()    # Destroy the Tkinter root window

root.protocol("WM_DELETE_WINDOW", on_closing)  # Bind the close button to `on_closing`







# Main loop
root.mainloop()


