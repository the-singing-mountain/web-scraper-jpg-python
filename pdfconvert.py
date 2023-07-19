from bs4 import *
import requests
import os
import glob, os, re
from PIL import Image

def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]

def convert_to_pdf(folder_name):
    jpgfiles = []
    for _file in sorted(glob.glob("*.png"), key=os.path.getmtime):
        jpgfiles.append(_file)

    jpgfiles.sort(key = natural_keys)

    print(jpgfiles)
    images = [
        Image.open(str(f))
        for f in jpgfiles
    ]

    images = [
        f.convert('RGB')
        for f in images
    ]

    pdf_path = folder_name+".pdf"
    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )

    print("Process completed!")