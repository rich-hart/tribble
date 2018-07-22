import os
from os.path import dirname, realpath, join
import unittest
import argparse
import json
import numpy
import cv2
import cv
#https://github.com/kimmobrunfeldt/howto-everything/blob/master/remove-green.md
B_MEAN = 218
B_STDEV = 5.0
B_SIGMA = 2.9
G_MEAN = 218
G_STDEV = 5.0
G_SIGMA = 2.9
R_MEAN = 218
R_STDEV = 5.0
R_SIGMA = 2.9

def main(argv=None):
#    import ipdb; ipdb.set_trace()
    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('input', type=argparse.FileType('r'))
    parser.add_argument('output', type=argparse.FileType('wb+'), default='mask.png')
    parser.add_argument('stats', type=argparse.FileType('r'),default='screen.json')

    args = parser.parse_args(argv)
    settings = vars(args)
    captain_img = cv2.imread(settings['input'].name)
    blue, green, red = cv2.split(captain_img)
    stats = json.loads(settings['stats'].read())
    b_mask = intensity_mask(blue, stats['B_MEAN'], stats['B_STDEV'], stats['B_SIGMA'])    
    g_mask = intensity_mask(green, stats['G_MEAN'], stats['G_STDEV'], stats['G_SIGMA'])    
    r_mask = intensity_mask(blue, stats['R_MEAN'], stats['R_STDEV'], stats['R_SIGMA'])    
    mask_1 = cv2.bitwise_and(b_mask,g_mask)
    mask_2 = cv2.bitwise_and(b_mask,r_mask)
    mask = cv2.bitwise_and(mask_1,mask_2)
    #channels
    # numpy.all(a, axis=None, out=None, keepdims=<class numpy._globals._NoValue>)
    # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.all.html#numpy.all
#    b_mask = intensity_mask(blue, settings['b_mean'],settings['b_stdev'],settings['b_sigma'])
#    g_mask = intensity_mask(green, settings['g_mean'],settings['g_stdev'],settings['g_sigma'])
#    r_mask = intensity_mask(red, settings['r_mean'],settings['r_stdev'],settings['r_sigma'])
#    ret, green_threshold = cv2.threshold(green,MEAN+SIGMA*STDEV,255,cv2.THRESH_BINARY)
    kernel = numpy.ones((5,5),numpy.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(settings['output'].name,mask) 
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
        main([TEST_CAPTAIN,'mask.png', 'screen.json'])

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
