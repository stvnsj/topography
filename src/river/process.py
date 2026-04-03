"""
This module processes the files with format:

2000001	4081798.06	198050.711	856.89	r
2000002	4081797.575	198051.235	853.941	r
2000003	4081796.941	198051.9	853.681	r
2000004	4081795.199	198054.071	852.115	r
2000005	4081792.681	198056.798	849.915	r
2000006	4081789.516	198060.351	846.941	r
2000007	4081784.796	198065.647	842.301	r

Where each number point is preceeded by the 
axis number in the millions place
"""


import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import utils


def process_river (input_file, output_file) :


    data     = np.genfromtxt(input_file, delimiter=',', skip_header=0, invalid_raise=False)
    str_data = np.genfromtxt(input_file, delimiter=',', dtype=str, skip_header=0,invalid_raise=False)



    def is_int(s):
        try:
            n = int(s)
            return True
        except:
            return False



    sorted_index = data[:,0].argsort()


    str_data = str_data[sorted_index]
    data = data[sorted_index]


    for row in data:
        row[0] = np.floor_divide(row[0] , 1000000)



    str_data[:,0] = data[:,0]



    start_points = [0]
    end_points   = []


    # GET START POINTS
    K = 0
    while (K != len(data) - 1):
        if data[K][0] != data[K+1][0]:
            start_points.append(K+1)
        K += 1

    # GET END POINTS
    i = 0
    while i < len(data) :
        if is_int(data[i][4]):
            end_points.append(i)
        i += 1




    # print("start points")
    # print(start_points)



    # print("end points")
    # print(end_points)


    for i in range(len(end_points)):
        str_data[[start_points[i],end_points[i]]] = str_data[[end_points[i],start_points[i]]]
        data[[start_points[i],end_points[i]]] = data[[end_points[i],start_points[i]]]



    for i in range(len(str_data)):
        if not is_int(str_data[i][4]):
            str_data[i][4] = str_data[i][4] + "-d"
            str_data[i][0] = ""


    np.savetxt(output_file, str_data, delimiter=',', fmt='%s')




    # Extract columns
    groups = data[:, 0]
    x = data[:, 1]
    y = data[:, 2]

    # Create a scatter plot
    plt.figure(figsize=(8, 6))

    # Unique group numbers
    unique_groups = np.unique(groups)

    # Assign a distinct color to each group
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_groups)))

    for group, color in zip(unique_groups, colors):
        mask = groups == group
        plt.scatter(x[mask], y[mask], s=10, color=color, label=f'Perfil {int(group)}')

    # Add legend and labels
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Plot de puntos por perfil')

    # Save the figure instead of showing it
    output_filename = utils.changeExtension(output_file, "png")
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')

    # Close the figure to free memory
    plt.close()

    print(f"Análisis gráfico de consistencia: {output_filename}")


def main () :
    process_river()
     

if __name__ == "__main__" :
    main () 