import os
from os.path import dirname, realpath, join
import unittest
import argparse
import json
import numpy
import cv2
import cv
DATA_DIR = join(dirname(realpath(__file__)),'data')
RESOURCE_DIR = join(DATA_DIR,'resources')
FAN_PICTURE = os.path.join(RESOURCE_DIR, 'FAN-PIC.png')
BACKGROUND_WALL = join(RESOURCE_DIR,'background_wall.png')
BACKGROUND_TRIBBLES = join(RESOURCE_DIR,'background_tribbles.png')
FORGROUND_TRIBBLES = join(RESOURCE_DIR,'forground_tribbles.png')
FORGROUND_BORDER_AND_LOGO = join(RESOURCE_DIR,'forground_border_and_logo.png')
OUTPUT = join(RESOURCE_DIR, 'merged_images.png')

   
def main(argv=None):
#    import ipdb; ipdb.set_trace()
    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('image', type=argparse.FileType('rb'))
    parser.add_argument('--output', type=argparse.FileType('wb+'), default = 'resized_image.png')
   
    args = parser.parse_args(argv)
    settings = vars(args)

    img = cv2.imread(settings['image'].name)
    resized_img = cv2.resize(img, (2100,1500))
    cv2.imwrite(settings['output'].name, resized_img)
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
