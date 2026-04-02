
from pathlib import Path


import json


def read_config () :
    with open("configuration.json", "r") as file:
        data = json.load(file)
        print(data)


def read_loaded_files (field) :
    
    with open("configuration.json", "r") as file:
        data = json.load(file)
    
    val = data['loaded-files'][field]
    return "" if val is None else val



def write_loaded_files (field,newpath):
    with open("configuration.json", "r") as file:
        data = json.load(file)
    
    data['loaded-files'][field] = str(Path(newpath)) if newpath else ""
    
    # Write the updated data back to the file
    with open("configuration.json", "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    print("config.py module\n==================")
    read_loaded_files('cotas-pr')
    write_loaded_files('cotas-pr','/home/jstvns/file.csv')
    read_loaded_files('cotas-pr')
