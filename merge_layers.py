import os
from os.path import dirname, realpath, join
import unittest
import argparse
import json
import numpy
import cv2
import cv
#FIXME: alpha conditional stmt
def merge_imgs(img1,img2):
    rows,cols,channels_1 = img1.shape
    rows,cols,channels_2 = img2.shape

    for i in range(0,rows):
        for j in range(0,cols):
            if channels_2==4 and img2[i,j,3]==255:
                img1[i,j,0] = img2[i,j,0]            
                img1[i,j,1] = img2[i,j,1]            
                img1[i,j,2] = img2[i,j,2]            
#            img1[i,j,3] = img2[i,j,3]            
      
def main(argv=None):
#    import ipdb; ipdb.set_trace()
    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('layers', type=str,  nargs='+')
    parser.add_argument('--output', type=argparse.FileType('wb+'), default = 'merged_images.png')
   
    args = parser.parse_args(argv)
    settings = vars(args)
    layers = settings['layers']
    total_layers = len(layers)
    final_image = cv2.imread(layers.pop(0),-1)

    for layer in layers:
        img = cv2.imread(layer,-1)
        merge_imgs(final_image,img)
 
    cv2.imwrite(settings['output'].name,final_image) 
    return settings



DATA_DIR = join(dirname(realpath(__file__)),'data')
TEST_DATA = join(DATA_DIR,'resources')
TEST_FAN_PICTURE = os.path.join(TEST_DATA, 'FAN-PIC.png')
TEST_BACKGROUND_WALL = join(TEST_DATA,'background_wall.jpg')
TEST_BACKGROUND_TRIBBLES = join(TEST_DATA,'background_tribbles.png')
TEST_FORGROUND_TRIBBLES = join(TEST_DATA,'forground_tribbles.png')
TEST_FORGROUND_BORDER_AND_LOGO = join(TEST_DATA,'forground_border_and_logo.png')
TEST_OUTPUT = join(TEST_DATA, 'merged_images.png')

class TestTribbify(unittest.TestCase):
 
    def test(self):
        pass

    def test_main(self):
        main([TEST_BACKGROUND_WALL,TEST_BACKGROUND_TRIBBLES,TEST_FAN_PICTURE,TEST_FORGROUND_TRIBBLES,TEST_FORGROUND_BORDER_AND_LOGO,'--output='+TEST_OUTPUT])

if __name__ == "__main__":
    main()
