import imgConverter
import os
import glob
import sys
import shutil

def create_empty_structure(src_dir, appendix = "_copy"):
    # Define the destination directory as the source directory name with an "_empty" suffix
    dest_dir = src_dir + appendix
    for root, dirs, _ in os.walk(src_dir):
        # Compute the relative path to the source directory
        relative_path = os.path.relpath(root, src_dir)
        # Create the corresponding directory in the destination
        new_dir = os.path.join(dest_dir, relative_path)
        os.makedirs(new_dir, exist_ok=True)
    return dest_dir




def annex9_process_geo (input_dir,crop_zoom=1.5):
    dest_directory = create_empty_structure(input_dir, appendix="copy")
    src_directory  = input_dir
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            src_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(src_file_path, src_directory)
            dest_file_path = os.path.join(dest_directory, relative_path)
            POINT, ext = os.path.splitext(file)
            if "_g." in src_file_path:
                imgConverter.adjust_annex9_geo(src_file_path,dest_file_path, POINT = POINT)
            if "_p." in src_file_path:
                imgConverter.adjust_annex9_panoramic(src_file_path,dest_file_path)
            if "_a." in src_file_path:
                imgConverter.adjust_annex9_detail(src_file_path,dest_file_path,crop_zoom=crop_zoom)
    return dest_directory

def annex9_process (input_dir,crop_zoom=1.5):
    dest_directory = create_empty_structure(input_dir)
    src_directory = input_dir
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            src_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(src_file_path, src_directory)
            dest_file_path = os.path.join(dest_directory, relative_path)
            if "_p." in src_file_path:
                imgConverter.adjust_annex9_panoramic(src_file_path,dest_file_path)
            if "_a." in src_file_path:
                imgConverter.adjust_annex9_detail(src_file_path,dest_file_path,crop_zoom=crop_zoom)
    return dest_directory



def annex2_process_geo (input_dir,crop_zoom=1.5):
    dest_directory = create_empty_structure(input_dir, appendix="_copy")
    src_directory  = input_dir
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            src_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(src_file_path, src_directory)
            dest_file_path = os.path.join(dest_directory, relative_path)
            POINT, ext = os.path.splitext(file)
            if "_g." in src_file_path:
                imgConverter.adjust_annex2_geo(src_file_path,dest_file_path, POINT = POINT)
            if "_p." in src_file_path:
                imgConverter.adjust_annex2_panoramic(src_file_path,dest_file_path)
            if "_a." in src_file_path:
                imgConverter.adjust_annex2_detail(src_file_path,dest_file_path,crop_zoom=crop_zoom)
    return dest_directory


def annex2_process (input_dir,crop_zoom=1.5):
    dest_directory = create_empty_structure(input_dir)
    src_directory = input_dir
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            src_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(src_file_path, src_directory)
            dest_file_path = os.path.join(dest_directory, relative_path)
            if "p." in src_file_path:
                imgConverter.adjust_annex2_panoramic(src_file_path,dest_file_path)
            if "a." in src_file_path:
                imgConverter.adjust_annex2_detail(src_file_path,dest_file_path,crop_zoom=crop_zoom)
    return dest_directory

def annex5_process_geo (input_dir,crop_zoom=1.5):
    dest_directory = create_empty_structure(input_dir, appendix="copy")
    src_directory  = input_dir
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            src_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(src_file_path, src_directory)
            dest_file_path = os.path.join(dest_directory, relative_path)
            POINT, ext = os.path.splitext(file)
            if "_g." in src_file_path:
                imgConverter.adjust_annex5_geo(src_file_path,dest_file_path, POINT = POINT)
            if "_p." in src_file_path:
                imgConverter.adjust_annex5_panoramic(src_file_path,dest_file_path)
            if "_a." in src_file_path:
                imgConverter.adjust_annex5_detail(src_file_path,dest_file_path,crop_zoom=crop_zoom)                
    return dest_directory

def annex5_process (input_dir,crop_zoom=1.5):
    dest_directory = create_empty_structure(input_dir)
    src_directory = input_dir
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            src_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(src_file_path, src_directory)
            dest_file_path = os.path.join(dest_directory, relative_path)

    return dest_directory

if __name__ == "__main__":
    print("annexImg.py")
