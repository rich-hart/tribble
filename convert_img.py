import os
from os.path import dirname, realpath, join
import unittest
import argparse
import json
import numpy
import cv2
import cv

import rawpy
import imageio
from rawphoto.cr2 import Cr2

   
def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('image', type=argparse.FileType('rb'))
    parser.add_argument('--output', type=argparse.FileType('wb+'), default = 'converted_image.png')
   
    args = parser.parse_args(argv)
    settings = vars(args)
#    img = cv2.imread(settings['image'].name)
    if '.cr2' in settings['image'].name.lower():
        raw = rawpy.imread(settings['image'].name)
        rgb = raw.postprocess()
        imageio.imsave(settings['output'].name, rgb)    
    elif '.jpg' in settings['image'].name.lower():
        img = cv2.imread(settings['image'].name)
        cv2.imwrite(settings['output'].name, img)
    return settings



if __name__ == "__main__":
    main()
