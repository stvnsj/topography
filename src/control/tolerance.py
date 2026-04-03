import numpy as np

descr_tol = {
    "rs"  : 0.010,
    "P-s" : 0.010,
    "ll"  : 0.010,}

# DENTRO DE TOLERANCIA ?
def within_tol (descr, y_ctrl, y_proj) :

    try:
        tol = descr_tol[descr]
    except:
        print(f'Descriptor {descr_tol} sin tolerancia asociada --> Fuera de tolerancia')
        return False
    
    delta = np.abs(y_ctrl - y_proj)
    
    if delta > tol:
        return False
    
    return True





def main() :
    pass





if __name__ == "__main__":
    main()
