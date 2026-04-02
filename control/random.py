import control.model       as control_model
import refactorModel.model as mdl

import numpy as np


def assign_weight (row, positive = True):
    
    # Not a control point
    if row[6] == "0":
        return 0
    
    # Axis row
    if row[0] != "":
        return 0
    
    distance = float(row[1])
    
    if positive and distance <= 0.000:
        return 0
    if not positive and distance >= 0.000:
        return 0


    #######################################
    if np.abs(distance) < 0.001:
        return 0
    if np.abs(distance) < 6.000:
        return 10
    if np.abs(distance) < 9.000:
        return 7
    if np.abs(distance) < 12.000:
        return 4
    else:
        return 2


def build_distribution (matrix,positive=True) :
    
    if positive:
        weights = np.array(list(map(lambda r : assign_weight(r), matrix)))
    else:
        weights = np.array(list(map(lambda r : assign_weight(r,positive=False), matrix)))
        
    distribution = weights / sum(weights)
    return distribution

class RandomSection :
    def __init__ (self, dm, matrix):
        self.dm = dm
        self.matrix = matrix

class RandomModel :
    def __init__ (self, cmodel):
        
        
        self.sections = []
        
        for sec in control_model.ModelIterator(cmodel):
            try:
                
                dm = sec.dm
                
                positive_distribution = build_distribution(sec.matrix,positive=True)
                negative_distribution = build_distribution(sec.matrix,positive=False)
                
                positive_indices = np.random.choice(np.arange(len(sec.matrix)), size=3, replace=False, p=positive_distribution)
                negative_indices = np.random.choice(np.arange(len(sec.matrix)), size=3, replace=False, p=negative_distribution)
                
                matrix = np.vstack((sec.matrix[positive_indices],sec.matrix[negative_indices]))
                matrix[:,0] = dm
                self.sections.append(RandomSection(sec.dm,matrix))
            except:
                print(f">> Advertencia: No se pudo seleccionar puntos aleatorios para dm {sec.dm}")
    
    def write_random_control (self, filename="TestControl.csv"):
        with open(filename, mode="w") as file:
            for sec in self.sections:
                np.savetxt(file, sec.matrix, delimiter=",", fmt="%s")  # Specify format as needed


def main () :
    
    coor_topo = "/home/jstvns/eqc-input/auto-control/coor-topo.csv"
    coor_ctrl = "/home/jstvns/eqc-input/auto-control/coor-ctrl.csv"
    longitudinal = "/home/jstvns/eqc-input/auto-control/longitudinal.csv"
    
    model1 = mdl.Model(
        filename1 = "", # DESCR
        filename2 = coor_topo, # COOR
        filename3 = longitudinal, # LONG
    )
    
    model2 = mdl.Model(
        filename1 = "",
        filename2 = coor_ctrl,
        filename3 = longitudinal,
    )
    
    cmodel = control_model.ControlModel(model1,model2)
    rmodel = RandomModel(cmodel)
    rmodel.write_random_control()


if __name__ == "__main__":
    print("control.random")
    main()
