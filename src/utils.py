import numpy as np
import re
import os




def changeExtension (filepath : str, newExtension : str) : 
    new_filename = os.path.splitext(filepath)[0] + f".{newExtension}"
    return new_filename


import re

import re

def normalize_pr(s: str) -> str:
    """
    Take any string starting with “pr”, “t” or “g” (any case), find the first integer in it,
    then keep the rest of the string (dropping spaces, hyphens, underscores) in upper case.
    Returns "<PREFIX><that_integer><SUFFIX_CLEANED>".
    """
    # (?i)             → case-insensitive
    # ^(pr|t|g)        → capture prefix "pr", "t" or "g"
    # .*?              → skip as few chars as needed until…
    # (\d+)            → capture the integer
    # (.*)$            → capture the rest of the string (including separators)
    m = re.search(r'(?i)^(pr|t|g).*?(\d+)(.*)$', s)
    if not m:
        raise ValueError(f"No PR/T/G<number> pattern found in {s!r}")

    prefix = m.group(1).upper()
    num    = int(m.group(2))              # strip leading zeros
    suffix = m.group(3)                   # what follows the integer

    # remove spaces, hyphens, underscores, then uppercase
    clean_suffix = re.sub(r'[ _-]+', '', suffix).upper()

    return f"{prefix}{num}{clean_suffix}"



normalize_pr_array = np.vectorize(normalize_pr)




class AxisError(Exception):
    """Custom exception with an optional message."""
    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)

def euc_dist (x1,y1,x2,y2) :
    s1 = np.square(x1 - x2)
    s2 = np.square(y1 - y2)
    D = np.sqrt(s1 + s2)
    return np.round(D,3)
    


def str_to_flt(s):
    try:
        return np.round(np.float64(s),3)
    except:
        raise AxisError(f'El valor {s} no puede convertirse en número')
    

def str_to_flt_arr (s) :
    return np.round(s.astype(float), 3)
    
    
    # try:
    #     return np.round(s.astype(float), 3)
    # except:
    #     print(s)
    

class CustomError(Exception):
    pass

#def normalize_pr(string):
#    # Check if the string starts with "PR" (case-insensitive) followed by optional spaces/hyphens and an integer
#    match = re.match(r'(?i)^pr[\s-]*\d+$', string.strip())
#    if match:
#        # Extract the number part from the string
#        number = re.search(r'\d+', string).group(0)
#        return f"PR{number}"
#    else:
#        raise CustomError(f"PR erróneo: {string}")



class Reporter :
    
    def __init__ (self, filename):
        self.path = self.__init_file_path__(filename)
    
    def __init_file_path__ (self, filename) :
        
        output_filename_ext = os.path.basename(filename)
        output_filename , ext    =  os.path.splitext(output_filename_ext)
        parent_dir = os.path.dirname(os.getcwd())
        target_dir = os.path.join(parent_dir, 'log')
        file_path = os.path.join(target_dir, output_filename)
        return file_path + ".txt"
    
    def write_report_header (self, filename) :
        name = os.path.basename(filename)
        with open(self.path, 'w') as f:
            f.write(f"Reporte de {name}\n\n")
    
    def patchFound (self, dm, direction, patch):
        with open(self.path, 'a') as f:
            f.write(f'DM {dm} parchado con altura {patch} en cota de {direction}\n')
    
    def patchNotFound (self,dm,direction):
        with open(self.path, 'a') as f:
            f.write(f'DM {dm} sin cota de {direction}\n')



formatFloat      = lambda x : f'{np.round(x,3)}'
formatFloatArray = lambda array : np.vectorize(formatFloat)(array)

# RESTORE THE CORRECT DIRECTION
# TODO TODO TODO TODO TODO TODO
def compute_sign (v1, v2):
    
    x1 = v1[0]
    y1 = v1[1]
    
    x2 = v2[0]
    y2 = v2[1]
 
    prod = x1 * y2 - y1 * x2
    
    if prod > 0:
        return -1
    else:
        return 1

compute_sign_array = np.vectorize(compute_sign,signature='(n),(n)->()')



def parseLabel(label):
    
    if label.endswith("i") or label.endswith("I"):
        return -1
    
    else:
        return 1


def parseLabelLetter(label):
    if label.endswith("i") or label.endswith("I"):
        return "l"
    elif label.endswith("d") or label.endswith("D"):
        return "r"
    else:
        return "e"  

parseLabelArray = np.vectorize(parseLabel)
parseLabelLetterArray = np.vectorize(parseLabelLetter)

def round_float (x):
    """round float to three decimal places"""
    return np.round(x,3)

def format_float (x):
    """float to string with three decimal places"""
    return "{:.3f}".format(x)

def format_float_array (arr):
    """floats of array to string with three decimal places"""
    return np.vectorize(format_float)(arr)



# Function to extract the numeric part of PR points
def pr_number(s):
    # Use regular expression to find the number in the string
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())
    return None

def label_num(s):
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())
    return None


def normalize_fstring(s):
    """Converts a string decimal number to the
    normal representation, like 13.300"""
    try:
        # The string number is cleaned of any trailing or leading spaces.
        # It is converted to a float, which succeeds if representation is valid.
        # It is rounded to the the third decimal.
        # It is returned as a decimal representation with three decimals.
        number = np.round(np.float64(s.strip()),3)
        return f"{number:.3f}"
    except:
        # If string does not represents a valid number, it is returned
        # as it is.
        return s


def is_float(s):
    """Checks whether input can be cast from string to float"""
    try:
        float(s)
        return True
    except ValueError:
        return False


def normalize_fstring_array(arr):
    return np.vectorize(normalize_fstring)(arr)

def read_csv (input_file, cols=None):
    """normalizes string decimal numbers into the format 23.120 (three decimals).
    Other strings are left as they are. It returns a string matrix."""
    matrix = np.genfromtxt(input_file, delimiter=',', dtype=str, skip_header=0, invalid_raise=False, usecols=cols)
    return normalize_fstring_array(matrix)

def write_csv(filename, matrix, mode = 'w', header = ""):
    """writes a numpy array into a csv file"""
    with open(filename, mode=mode) as file:
        np.savetxt(file, matrix, delimiter=",", fmt="%s" , header = header)


def round (x) :
    return np.round(x,3)


def clean_descriptor(s):
    # Strip trailing whitespace
    s = s.rstrip()
    
    # Check for and remove the specific trailing substrings
    for suffix in ["-i", "-I", "-d", "-D"]:
        if s.endswith(suffix):
            s = s[: -len(suffix)]
            break  # Exit the loop since we found and removed the suffix
    
    return s.strip()  # Final strip to handle any leftover whitespace

if __name__ == "__main__":
    arr = np.array([
        [1,2,34],
        [3,2,1],
        [0,0,0]
    ])
    write_csv('csv_test.csv', arr)
