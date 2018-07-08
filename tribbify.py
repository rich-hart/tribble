import os
from os.path import dirname, realpath, join
import unittest
import argparse

import cv2
import cv
B_MEAN = 218
B_STDEV = 10.0
B_SIGMA = 2.9
G_MEAN = 218
G_STDEV = 10.0
G_SIGMA = 2.9
R_MEAN = 218
R_STDEV = 10.0
R_SIGMA = 2.9

def main(argv=None):
#    import ipdb; ipdb.set_trace()
    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('captain', type=file)
    args = parser.parse_args(argv)
    settings = vars(args)
    captain_img = cv2.imread(settings['captain'].name)

    #channels
#    blue, green, red = cv2.split(captain_img)
#    ret, green_threshold = cv2.threshold(green,MEAN+SIGMA*STDEV,255,cv2.THRESH_BINARY)    
    return settings


def intensity_mask(img, mean, stdev, sigma):
    ret, threshold = cv2.threshold(img, mean - sigma * stdev,255,cv2.THRESH_BINARY)
    ret, threshold_inv = cv2.threshold(img,mean + sigma * stdev,255, cv2.THRESH_BINARY_INV)
    mask = cv2.bitwise_and(threshold, threshold_inv)
   
    return mask # mask

TEST_DIR = join(dirname(realpath(__file__)),'tests')
TEST_DATA = os.path.join(TEST_DIR,'data')
TEST_CAPTAIN = os.path.join(TEST_DATA, 'captain.png')

class TestTribbify(unittest.TestCase):
    def setUp(self):
        self.captain_img = cv2.imread(TEST_CAPTAIN)
        self.blue, self.green, self.red = cv2.split(self.captain_img)
 
    def test(self):
        pass

    def test_main(self):
        main([TEST_CAPTAIN])

    def test_intensity_mask_blue(self):
#        captain_img = cv2.imread(TEST_CAPTAIN)
#        blue, green, red = cv2.split(self.captain_img)
        returned = intensity_mask(self.blue, B_MEAN, B_STDEV, B_SIGMA)
        cv2.imwrite( os.path.join(TEST_DATA, 'test_intensity_mask_blue.png'),returned)

    def test_intensity_mask_green(self):
#        captain_img = cv2.imread(TEST_CAPTAIN)
#        blue, green, red = cv2.split(self.captain_img)
        returned = intensity_mask(self.green, G_MEAN, G_STDEV, G_SIGMA)
        cv2.imwrite( os.path.join(TEST_DATA, 'test_intensity_mask_green.png'),returned)

    def test_intensity_mask_red(self):
#        captain_img = cv2.imread(TEST_CAPTAIN)
#        blue, green, red = cv2.split(self.captain_img)
        returned = intensity_mask(self.red, R_MEAN, R_STDEV, R_SIGMA)
        cv2.imwrite( os.path.join(TEST_DATA, 'test_intensity_mask_red.png'),returned)

if __name__ == "__main__":
    unittest.main()
