import numpy as np
import utils

def choose_random_atom (choices, weights) :
    choice  = np.random.choice(choices, size=1, replace=True, p=weights)
    return choice[0]

def choose_random_array (choices, weights=None, size=1) :
    if weights is None:
        weights = [x for x in []]
    choices  = np.random.choice(choices, size=size, replace=True, p=weights)
    return np.array(choices)

def main () :
    
    filename = '/home/jstvns/axis/eqc-input/control-eje-estaca/eje-estaca-proj-sub.csv'
    matrix   = utils.read_csv(filename)
    N = len(matrix)
    choices = [0.000 , 0.010, 0.020, 0.030, 0.040, 0.050, 0.060, ]
    weights = [0.100 , 0.200, 0.200, 0.200, 0.100, 0.100, 0.100, ]
    
    delta_x = choose_random_array(choices,weights,N)
    delta_y = choose_random_array(choices,weights,N)
    
    x = matrix[:,1].astype(float) + delta_x
    y = matrix[:,2].astype(float) + delta_y

    matrix[:,1] = utils.format_float_array (x)
    matrix[:,2] = utils.format_float_array (y)
    
    utils.write_csv('/home/jstvns/axis/eqc-input/control-eje-estaca/eje-estaca-ctrl.csv', matrix)
    
    

def main1 () :
    
    filename = '/home/jstvns/axis/eqc-input/control-level/longi-proj-sub.csv'
    matrix   = utils.read_csv(filename)
    N = len(matrix)
    choices = [0.000 , 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, ]
    weights = [0.100 , 0.200, 0.200, 0.200, 0.100, 0.100, 0.100, ]
    arr = choose_random_array(choices,weights,N)
    matrix[:,1] = utils.format_float_array(matrix[:,1].astype(float) + arr)
    utils.write_csv('/home/jstvns/axis/eqc-input/control-level/longi-ctrl-complete.csv', matrix)
    
    
if __name__ == '__main__':
    main()
