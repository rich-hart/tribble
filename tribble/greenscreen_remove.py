"""
Removes greenscreen from an image.
Usage: python greenscreen_remove.py image.jpg
"""

from PIL import Image
import sys
import os
import argparse

def rgb_to_hsv(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, s, v




def main(argv=None):
    # Load image and convert it to RGBA, so it contains alpha channel
    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('file_path', type=argparse.FileType('rb'))
    parser.add_argument('-min_h', '--min_hue', type=int, default=100)
    parser.add_argument('-min_s', '--min_saturation', type=int, default=80)
    parser.add_argument('-min_v', '--min_value', type=int, default=70)
    parser.add_argument('-max_h', '--max_hue', type=int, default=185)
    parser.add_argument('-max_s', '--max_saturation', type=int, default=255)
    parser.add_argument('-max_v', '--max_value', type=int, default=190)

#    parser.add_argument('--output', type=argparse.FileType('wb+'))
    args = parser.parse_args(argv)
    settings = vars(args)
    GREEN_RANGE_MIN_HSV = (settings['min_hue'], settings['min_saturation'], settings['min_value'])
    GREEN_RANGE_MAX_HSV = (settings['max_hue'], settings['max_saturation'], settings['max_value'])
    file_path = settings['file_path'].name
    name, ext = os.path.splitext(file_path)
    im = Image.open(file_path)
    im = im.convert('RGBA')

    # Go through all pixels and turn each 'green' pixel to transparent
    pix = im.load()
    width, height = im.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = pix[x, y]
            h_ratio, s_ratio, v_ratio = rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            h, s, v = (h_ratio * 360, s_ratio * 255, v_ratio * 255)

            min_h, min_s, min_v = GREEN_RANGE_MIN_HSV
            max_h, max_s, max_v = GREEN_RANGE_MAX_HSV
            if min_h <= h <= max_h and min_s <= s <= max_s and min_v <= v <= max_v:
                pix[x, y] = (0, 0, 0, 0)


    im.save(name + '.png')


if __name__ == '__main__':
    main()

