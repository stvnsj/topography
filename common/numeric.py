

import numpy as np 

def to_float(value):
    try:
        return float(value)
    except Exception:
        return None

def to_rounded_float(value, decimals=3):
    number = to_float(value)
    if number is None:
        return None
    return np.round(number, decimals)

def are_close(a, b, tolerance=0.01):
    return np.abs(a - b) <= tolerance