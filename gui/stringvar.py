
import tkinter as tk
from .rootFrame import root


cerco_switch = tk.BooleanVar(value=False)



descriptor_file = tk.StringVar() # TRANS DESCRIPTOR
coordinate_file = tk.StringVar() # TRANS COORDENADA
longitudinal_file = tk.StringVar() # Longitudinal FILE
plot_index = tk.StringVar() # Current 
eje_estaca_file = tk.StringVar() 
img_dir1 = tk.StringVar()
img_dir2 = tk.StringVar()
master_table_file = tk.StringVar()
pr_level_file  = tk.StringVar() 
pr_height_file = tk.StringVar()
libreta_file   = tk.StringVar()
trigonometric_file = tk.StringVar()
master_pr_file = tk.StringVar()


# ******** CONTROL FIELDS *********
mop_proj_file = tk.StringVar()
mop_ctrl_file = tk.StringVar()

level_proj_file = tk.StringVar()
level_ctrl_file = tk.StringVar()

mdt_proj_file = tk.StringVar()
mdt_ctrl_file = tk.StringVar()

axis_proj_file = tk.StringVar()
axis_ctrl_file = tk.StringVar()

random_seed_input   = tk.StringVar()
random_seed_input.set("42")

detail_image_zoom = tk.StringVar()
detail_image_zoom.set("1.5")


project_length_input = tk.StringVar()
dm_interval_input = tk.StringVar()
# *********************************



meter0 = tk.StringVar()
meter1 = tk.StringVar()
chunkSize = tk.StringVar()
stackLength = tk.StringVar()
projectName = tk.StringVar()
yscale = tk.StringVar()
yscale.set("1.0")



# --------------------------
mop_to_ter = tk.StringVar()
river_axis = tk.StringVar()
libreta_app = tk.StringVar()


