"""
This module converts MOP format to TER format.
"""
import utils
import numpy as np
import sys
import os

def generate_ter (input_file, output_file) :

    mop_matrix = utils.read_csv(input_file)
    
    START = 0
    END   = 0
    INDEX = 1
    
    N = len(mop_matrix)
    
    with open(output_file, "w") as f:
        
        while (INDEX < N):
            
            if mop_matrix[INDEX][0] != "" or INDEX == N-1 :
                
                if INDEX == N-1:
                    INDEX += 1
                
                START = END 
                END = INDEX
                
                sorted_indices = np.argsort(mop_matrix[START:END][:, 1].astype(float))
                
                head_row   = mop_matrix[START]
                f.write(f" {head_row[0]},{END-START},0,0 \n")
                
                for row in mop_matrix[START:END][sorted_indices]:
                    f.write(f" {row[1]},{row[2]} \n")
            
            INDEX += 1
    return 1




def main () :
    
    input_file = sys.argv[1]
    
    # Change extension to .ter while keeping the base filename
    base_name = os.path.splitext(input_file)[0]  # Remove the .csv extension
    output_file = f"{base_name}.ter"  # Add .ter extension

    generate_ter(input_file, output_file)
    print(f"Converted {input_file} → {output_file}")

if __name__ == "__main__":
    main()
