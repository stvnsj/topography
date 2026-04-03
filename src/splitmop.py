


import utils
import numpy as np

# I must select two non-intersecting points from this coordinate file.
matrix = utils.read_csv('/home/jstvns/eqc-input/auto-control/coor-original.csv')

matrix_topo = np.empty((0,5))
matrix_control = np.empty((0,5))


for row in matrix:
    
    if row[0] != "":
        matrix_topo = np.vstack((matrix_topo, row))
        matrix_control = np.vstack((matrix_control, row))
        continue
    
    if np.random.choice([0,1]) :
        print("topo assignment of row")
        print(row)
        print("-------------------------")
        matrix_topo = np.vstack((matrix_topo, row))
    else:
        print("ctrl assignment of row")
        print(row)
        print("--------------------------")
        matrix_control = np.vstack((matrix_control, row))

np.savetxt("/home/jstvns/eqc-input/auto-control/coor-topo.csv", matrix_topo, delimiter=",", fmt="%s")
np.savetxt("/home/jstvns/eqc-input/auto-control/coor-ctrl.csv", matrix_control, delimiter=",", fmt="%s")

