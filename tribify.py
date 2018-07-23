import os
from os.path import dirname, realpath, join, basename
import unittest
import argparse
import json
import numpy
import cv2
import cv
import subprocess
import tempfile

DATA_DIR = join(dirname(realpath(__file__)),'data')
RESOURCE_DIR = join(DATA_DIR,'resources')
FAN_PICTURE = os.path.join(RESOURCE_DIR, 'FAN-PIC.png')
BACKGROUND_WALL = join(RESOURCE_DIR,'background_wall.png')
BACKGROUND_TRIBBLES = join(RESOURCE_DIR,'background_tribbles.png')
FORGROUND_TRIBBLES = join(RESOURCE_DIR,'forground_tribbles.png')
FORGROUND_BORDER_AND_LOGO = join(RESOURCE_DIR,'forground_border_and_logo.png')
OUTPUT = join(RESOURCE_DIR, 'merged_images.png')

import contextlib
import os
import shutil
import tempfile

import convert_img

WIDTH = 2100 #1728 #2100
HEIGHT = 1500 # 1296 #1500
CHANNELS = 4

@contextlib.contextmanager
def cd(newdir, cleanup=lambda: True):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
        cleanup()

@contextlib.contextmanager
def tempdir():
    dirpath = tempfile.mkdtemp()
    def cleanup():
        shutil.rmtree(dirpath)
    with cd(dirpath, cleanup):
        yield dirpath

def main(argv=None):
    import ipdb; ipdb.set_trace()
    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('fan_picture', type=argparse.FileType('rb'))
#    parser.add_argument('--output', type=argparse.FileType('wb+'))
    args = parser.parse_args(argv)
    settings = vars(args)
#    with tempdir() as temp_dir:
#        pass
    command = "python convert_img.py {} " \
              "--output /vagrant/src/tribble/converted_img.png".format(settings['fan_picture'].name).strip()
    subprocess.call(command.split(' ')) 
    command = "python resize_img.py /vagrant/src/tribble/converted_img.png --output /vagrant/src/tribble/resized_img.png"  
    subprocess.call(command.split(' ')) 

    command = "python greenscreen_remove.py /vagrant/src/tribble/resized_img.png"
    subprocess.call(command.split(' '))

    command = "python merge_layers.py /vagrant/src/tribble/WALL.jpg /vagrant/src/tribble/TRIBBS_ON_BOTTOM.png /vagrant/src/tribble/resized_img.png /vagrant/src/tribble/TRIBBS_ON_TOP.png /vagrant/src/tribble/RAINBOW_BORDER.png /vagrant/src/tribble/GIS_LOGO.png --output /vagrant/src/tribble/merged_img.png"

    subprocess.call(command.split(' '))
    

    return settings



TEST_DIR = join(dirname(realpath(__file__)),'tests')
TEST_DATA = os.path.join(TEST_DIR,'data')
TEST_CAPTAIN = os.path.join(TEST_DATA, 'captain.png')

class TestTribbify(unittest.TestCase):
    def test_main(self):
        main([FAN_PICTURE])

if __name__ == "__main__":
    main()
