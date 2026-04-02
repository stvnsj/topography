"""

Brief description:
This module has functions that take a file a return a smaller randomly altered
file for control comparison purposes.

Detailed Description:

"""
import numpy as np
import utils
from control.range import ControlRangeList
from control.mop   import MopMatrixIterator



def random_sign ():
    choice = np.random.choice([1,-1], size=1, p=[0.5,0.5])
    return choice[0]

def binary_choice ():
    choice = np.random.choice([True,False], size=1, p=[0.5,0.5])
    return choice[0]

def choose_random_atom (choices, weights) :
    choice  = np.random.choice(choices, size=1, replace=True, p=weights)
    return choice[0]

def choose_random_array (choices, weights=None, size=1) :
    if weights is None:
        weights = [x for x in []]
    choices  = np.random.choice(choices, size=size, replace=True, p=weights)
    return np.array(choices)



def mop_ctrl_file (mop_file,  output_ctrl_file) :
    """Returns a randomly modified version of the provided eje-estaca file."""
    
    matrix = utils.read_csv(mop_file)
    mu, sigma = 0, 0.5 # mean and standard deviation
    
    for row in matrix:
        s = np.random.normal(mu, sigma, 1)[0]
        row[2] = utils.format_float(
            float(row[2]) + s
        )
    
    utils.write_csv(output_ctrl_file, matrix)



# filename is the name of a subset of eje-estaca filename.
def main (filename, output_filename) :
    """Returns a randomly modified version of the provided eje-estaca file."""
    
    # filename = '/home/jstvns/axis/eqc-input/control-eje-estaca/eje-estaca-proj-sub.csv'
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
    
    utils.write_csv(output_filename, matrix)




def main1 (filename, output_filename) :
    """Returns a randomly modified version of the provided longitudinal file."""
    # filename = '/home/jstvns/axis/eqc-input/control-level/longi-proj-sub.csv'
    matrix   = utils.read_csv(filename)
    N = len(matrix)
    choices = [0.000 , 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, ]
    weights = [0.100 , 0.200, 0.200, 0.200, 0.100, 0.100, 0.100, ]
    arr = choose_random_array(choices,weights,N)
    matrix[:,1] = utils.format_float_array(matrix[:,1].astype(float) + arr)
    utils.write_csv(output_filename, matrix)


if __name__ == '__main__':
    mop_ctrl_file(
        "/home/jstvns/axis/eqc-input/control-mdt/mop.csv",
        "/home/jstvns/axis/eqc-input/control-mdt/mop-ctrl.csv",
    )
