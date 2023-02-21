from bs4 import *
import requests
import os
import glob, os, re
from PIL import Image

# CREATE FOLDER
def folder_create(images, title):
    try:
        folder_name = title
        folder_name = re.sub('[^A-Za-z0-9 ]+', '', folder_name)
        folder_name = " ".join(folder_name.split())
        # folder creation
        os.mkdir(folder_name)

    # if folder exists with that name, ask another name
    except:
        print("Folder With That Name Exists!")
        folder_create()

    # image downloading start
    download_images(images, folder_name)

    convert_to_pdf(folder_name)

# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, folder_name):

    # initial count is zero
    count = 0

    # print total images found in URL
    print(f"Total {len(images)} Image Found!")

    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            # From image tag ,Fetch image Source URL
 
                        # 1.data-srcset
                        # 2.data-src
                        # 3.data-fallback-src
                        # 4.src

            # Here we will use exception handling

            # first we will search for "data-srcset" in img tag
            try:
                # In image tag ,searching for "data-srcset"
                image_link = image["data-srcset"]

            # then we will search for "data-src" in img
            # tag and so on..
            except:
                try:
                    # In image tag ,searching for "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # In image tag ,searching for "data-fallback-src"
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # In image tag ,searching for "src"
                            image_link = image["src"]
 
                        # if no Source URL found
                        except:
                            pass

            # After getting Image Source URL
            # We will try to get the content of image
            try:
                r = requests.get(image_link).content
                try:

                    # possibility of decode
                    r = str(r, 'utf-8')

                except UnicodeDecodeError:

                    # After checking above condition, Image Download start
                    with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                        f.write(r)

                    # counting number of image downloaded
                    count += 1
            except:
                pass

        # There might be possible, that all
        # images not download
        # if all images download
        if count == len(images):
            print("All Images Downloaded!")

        # if all images not download
        else:
            print(f"Total {count} Images Downloaded Out of {len(images)}")

# MAIN FUNCTION START
def main(url):

    # content of URL
    r = requests.get(url)

    # Parse HTML Code
    soup = BeautifulSoup(r.text, 'html.parser')

    # find all images in URL
    images = soup.findAll('img')
    title = soup.title.text

    # Call folder create function
    folder_create(images,title)

def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]

def convert_to_pdf(folder_name):
    jpgfiles = []
    for _file in sorted(glob.glob(folder_name+"/*.jpg"), key=os.path.getmtime):
        jpgfiles.append(_file)

    jpgfiles.sort(key = natural_keys)

    images = [
        Image.open(str(f))
        for f in jpgfiles
    ]

    images = [
        f.convert('RGB')
        for f in images
    ]

    pdf_path = folder_name+"/"+folder_name+".pdf"
    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )

    print("Process completed!")

# take url
url = input("Enter URL:- ")

# CALL MAIN FUNCTION
main(url)