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
#import numpy as np, cv
#vis = np.zeros((384, 836), np.float32)
#h,w = vis.shape
#vis2 = cv.CreateMat(h, w, cv.CV_32FC3)
#vis0 = cv.fromarray(vis)
def resize_img(img_path,temp_dir=''):
#    import ipdb;ipdb.set_trace()
    white_matrix = numpy.ones(( HEIGHT, WIDTH,CHANNELS),dtype=int) * int(255)
    resized_img_path = join(temp_dir,basename(img_path))
    img = cv2.imread(img_path)
#    img_c4 = cv2.cvtColor(src=img, code=cv2.CV_8UC4,dstCn=4)
    resized_img = cv2.resize(img,( WIDTH,HEIGHT))
    (h,w,c) = resized_img.shape
    for i in range(0,h):
       for j in range(0,w): 
           white_matrix[i,j,0] = resized_img[i,j,0]            
           white_matrix[i,j,1] = resized_img[i,j,1]            
           white_matrix[i,j,2] = resized_img[i,j,2]            
           if c ==4:
               white_matrix[i,j,3] = resized_img[i,j,3]
    resized_img = white_matrix       

    cv2.imwrite(resized_img_path,resized_img)
    return resized_img_path

def main(argv=None):

    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('fan_picture', type=argparse.FileType('rb'))
    parser.add_argument('--output', type=argparse.FileType('wb+'))
    args = parser.parse_args(argv)
    settings = vars(args)
    if not settings['output']:
        settings['output'] = join(dirname(settings['fan_picture'].name),'tribified_'+basename(settings['fan_picture'].name))

    with tempdir() as temp_dir:
        command = "python /vagrant/src/tribble/greenscreen_remove.py " + settings['fan_picture'].name
        subprocess.call(command.split(' '))
        command = "python /vagrant/src/tribble/merge_layers.py {0} {1} {2} {3} {4} --output={5}".format(
            resize_img(BACKGROUND_WALL),
            resize_img(BACKGROUND_TRIBBLES),
            resize_img(settings['fan_picture'].name),
            resize_img(FORGROUND_TRIBBLES),
            resize_img(FORGROUND_BORDER_AND_LOGO),
            settings['output'],
        )
        subprocess.call(command.split(' '))
    return settings



TEST_DIR = join(dirname(realpath(__file__)),'tests')
TEST_DATA = os.path.join(TEST_DIR,'data')
TEST_CAPTAIN = os.path.join(TEST_DATA, 'captain.png')

class TestTribbify(unittest.TestCase):
    def setUp(self):
        self.captain_img = cv2.imread(TEST_CAPTAIN)
        self.blue, self.green, self.red = cv2.split(self.captain_img)
 
    def test(self):
        pass

    def test_resize_img(self):
  #      import ipdb; ipdb.set_trace()
        resize_img(TEST_CAPTAIN)


    def test_main(self):
        main([FAN_PICTURE])

if __name__ == "__main__":
    main()
