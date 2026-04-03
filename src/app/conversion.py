"""
This module converts the android app's libreta 
to the format required by the computer program.

The phone libreta has the following format:

Starts and ends with:    
PRn   ,   Float   ,    ,  Float         (End Point)

Between PR's it has:  
Text  ,  Float ,       ,  Float         (Change Point)     OR
Text  ,        , Float ,                (Intermediate Point)
"""





import utils
import numpy as np
import sys



def starts_with_pr (point_name : str) -> bool: 
    return point_name.strip().lower().startswith("pr")





def convert_app_libreta (input_file,output_file) :

    # It is true while an interval is being transformed. 
    COPYING = False

    START_PR = ""
    END_PR   = ""


    py_matrix = np.empty((0, 6));



    app_matrix = utils.read_csv(input_file)

    "→"

    for row in app_matrix:

        if starts_with_pr(row[0]):
            if not COPYING:
                START_PR = row[0]
                COPYING = not COPYING
                new_row = np.array([row[0],"","",row[1],row[2],row[3]])
                py_matrix = np.vstack((py_matrix,new_row))
            else: # IF COPYING
                END_PR = row[0]
                COPYING = not COPYING
                new_row = np.array(["","",row[0],row[1],row[2],row[3]])
                py_matrix = np.vstack((py_matrix,new_row))
                print(f"Transformando de {START_PR} a {END_PR}")

        elif row[2] != "":
            new_row = np.array(["",row[0],"",row[1],row[2],row[3]])
            py_matrix = np.vstack((py_matrix,new_row))
        
        else : 
            new_row = np.array(["","","",row[1],row[2],row[3]])
            py_matrix = np.vstack((py_matrix,new_row))


    utils.write_csv(output_file, py_matrix)

def main () :
    convert_app_libreta(sys.argv[1],sys.argv[2])


if __name__ == "__main__" :
    main ()