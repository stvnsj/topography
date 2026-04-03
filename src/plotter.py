import matplotlib.pyplot as plt
import reader as rd
import model as md
import numpy as np
# import mplcursors


class Plotter :
    def __init__ (self, model) :
        self.model = model
    
    def plot_section2 (self, section_idx, fig, ax):
        
        ax.clear()
        section  = self.model.getSection(section_idx)
        
        # fig, ax = plt.subplots(figsize=(12, 12))
        min_z = np.min(section.adjustedHeight)
        max_z = np.max(section.adjustedHeight)
        delta_z = int(min_z) - 1
        h0 = min_z - delta_z
        indexList = np.argsort(section.distance);
        DIST = section.distance[indexList]
        HEIGHT = section.adjustedHeight[indexList]
        
        # SEA LINE
        ax.plot([DIST[0],DIST[-1]],[0,0], color='#e8e33f',linewidth=1)
        
        for i in range(len(DIST)):
            
            # VERTICAL LINES
            ax.plot([DIST[i],DIST[i]] , [0,  HEIGHT[i][0]-delta_z], color='#1f77b4',linewidth=1)
            
            
            #  DIST LABELS
            #plt.text(DIST[i], 0.0, f'{DIST[i]}', ha = 'left', va='top', fontsize=9, rotation=90, color='yellow')
            
            # DIST LABELS
            #plt.text(DIST[i], min_z, f'{DIST[i]}', ha = 'left', va='top', fontsize=9, rotation=90, color='yellow')
            
            
        # GROUND LINE 
        ax.plot(DIST , (HEIGHT - delta_z), color = "#ff5050",linewidth=1)
        ax = plt.gca()
        y_positions = np.arange(0, max_z-delta_z + 1, 1)
        y_labels = [f'{x + delta_z}' for x in y_positions]
        # Set the y-axis ticks at the specified positions
        ax.set_yticks(y_positions)
        ax.set_yticklabels(y_labels)
        fig.patch.set_facecolor('#2e2e2e')
        ax.set_facecolor('#2e2e2e')  # Sets the axes background color
        ax.tick_params(axis='both', colors='white', labelsize=10)  # Change x-axis tick labels color to red
        ax.spines['left'].set_color('white')   # Change left axis line color to blue
        ax.spines['right'].set_color('white')  # Change right axis line color to green
        ax.spines['top'].set_color('white')   # Change top axis line color to orange
        ax.spines['bottom'].set_color('white')   # Change top axis line color to orange
        ax.set_title(f"DM: {section.km}" , color="white")
        ax.grid(True, color='#5c5c5c', linestyle='--', linewidth=0.5)
        ax.set_xticks(DIST)
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_aspect('equal', adjustable='box')
        plt.show()
        
        
  
    def plot_section (
            self, 
            section_idx, 
            fig, 
            ax, 
            canvas
            ):
        
        ax.clear()
        
        section  = self.model.getSection(section_idx)
        
        # fig, ax = plt.subplots(figsize=(12, 12))
        min_z = np.min(section.adjustedHeight)
        max_z = np.max(section.adjustedHeight)
        delta_z = int(min_z) - 1
        h0 = min_z - delta_z
        indexList = np.argsort(section.distance);
        DIST = section.distance[indexList]
        HEIGHT = section.adjustedHeight[indexList]
        

        
        for i in range(len(DIST)):
            
            # VERTICAL LINES
            ax.plot([DIST[i],DIST[i]] , [0,  HEIGHT[i][0]-delta_z], color='#1f77b4',linewidth=1)
            
            
            #  DIST LABELS
            #plt.text(DIST[i], 0.0, f'{DIST[i]}', ha = 'left', va='top', fontsize=9, rotation=90, color='yellow')
            
            # DIST LABELS
            #plt.text(DIST[i], min_z, f'{DIST[i]}', ha = 'left', va='top', fontsize=9, rotation=90, color='yellow')
            
            
        # GROUND LINE 
        groundline = ax.plot(DIST , (HEIGHT - delta_z), color = "#ff5050",linewidth=1)
        # SEA LINE
        ax.plot([DIST[0],DIST[-1]],[0,0], color='#e8e33f',linewidth=1)
        
        ax = plt.gca()
        y_positions = np.arange(0, max_z-delta_z + 1, 1)
        y_labels = [f'{x + delta_z}' for x in y_positions]
        # Set the y-axis ticks at the specified positions
        ax.set_yticks(y_positions)
        ax.set_yticklabels(y_labels)
        fig.patch.set_facecolor('#2e2e2e')
        ax.set_facecolor('#2e2e2e')  # Sets the axes background color
        ax.tick_params(axis='both', labelsize=9)  # Change x-axis tick labels color to red
        ax.tick_params(axis='x', colors='#e8e33f')  # Change x-axis tick labels color to red
        ax.tick_params(axis='y', colors='#1f77b4')  # Change x-axis tick labels color to red
        ax.spines['left'].set_color('white')   # Change left axis line color to blue
        ax.spines['right'].set_color('white')  # Change right axis line color to green
        ax.spines['top'].set_color('white')   # Change top axis line color to orange
        ax.spines['bottom'].set_color('white')   # Change top axis line color to orange
        # ax.set_title(f"DM: {section.km}" , color="white")
        ax.grid(True, color='#5c5c5c', linestyle='--', linewidth=0.5)
        ax.set_xticks(DIST)
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_aspect('equal', adjustable='box')
        
        top_ax = ax.secondary_xaxis('top')
        top_ax.tick_params(labelrotation=90)
        # top_ax.set_xlabel("Top X-axis Label")  # Label for the top x-axis
        # Set custom tick labels for the top x-axis
        top_ax.set_color("white")
        top_positions = [0, 2, 4, 6, 8, 10]  # Positions for tick marks on the top axis
        top_labels    = [f'{z[0]}' for z in HEIGHT]  # Custom labels for top
        top_ax.set_xticks(DIST)
        top_ax.set_xticklabels(top_labels)
        top_ax.tick_params(colors='#ff5050', labelsize=9)
        
        # # Add mplcursors for hover annotation
        # cursor = mplcursors.cursor(groundline, hover=True)
        # cursor.remove_on_exit = True 
        
        # def on_add(sel):
        #     index = sel.index
        #     # Customize as per the DIST or HEIGHT, here using HEIGHT as example
        #     sel.annotation.set(text=f"Height: {HEIGHT[index][0] - delta_z}, Distance: {DIST[index]}")
            
        ax.figure.canvas.draw()
        

if __name__ == "__main__" :
    reader = rd.Reader ("/home/jstvns/axis/axis/dat-et.txt" , "", "/home/jstvns/axis/axis/longitudinal.txt")
    matrix, labels, om, ol, heights = reader.getData()
    model = md.Model(heights,matrix,labels, om, ol)
    print(model.get_km_index_dict())
    plotter = Plotter(model)

