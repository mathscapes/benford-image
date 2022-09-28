""" benstats2.py
    Benford Image Statistics
    
    Authors: @gv-sh @bhaumikdebanshu
    License: MIT

    Example:
    >>> python3 benstats2.py --dir=data --csv=csv/my_csv.csv --scale=0.25 --minmax=0,255 --floating_precision=3
"""

from ast import parse
import os
import pandas as pd
import cv2
import argparse

def benstats2(dir, csv, scale=1, minmax=(0, 255), floating_precision=8):
    """ Capture Benford Law analysis of all the jpgs/jpegs available in the given directory
    
        @param dir: Directory containing the images 
        @param csv: CSV file to store the results 

        @return None
    """

    files = [f for f in os.listdir(dir) if f.endswith('.jpg') or f.endswith('.jpeg')]

    batch = []

    for f in files:
        img = cv2.imread(os.path.join(dir, f))
        h,w = img.shape[:2]
        scale = 0.25
        img = cv2.resize(img, (int(w*scale), int(h*scale)), interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.normalize(gray, None, minmax[0], minmax[1], cv2.NORM_MINMAX)

        gray = gray.flatten();

        gray_firsts = [int(str(x)[0]) for x in gray]

        gray_benford = [gray_firsts.count(x) for x in range(1,10)]

        gray_benford_pct = [round(x*100/sum(gray_benford), floating_precision) for x in gray_benford]

        for i in range(1,10):
            batch.append({
                'image': f,
                'digit': i,
                'pct': gray_benford_pct[i-1]
            })

        print("Analysing image {} of {}..".format(files.index(f)+1, len(files)), end='\r')

    df = pd.DataFrame(batch)
    df.to_csv(csv, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Benford Image Statistics')
    parser.add_argument('--dir', type=str, help='Directory containing the images')
    parser.add_argument('--csv', type=str, help='CSV file to store the results')
    parser.add_argument('--scale', type=float, default=1, help='Scale factor for resizing the image')
    parser.add_argument('--minmax', type=str, default='0,255', help='Min and Max values for normalizing the image')
    parser.add_argument('--floating_precision', type=int, default=8, help='Floating precision for the percentages')

    args = parser.parse_args()

    benstats2(args.dir, args.csv, args.scale, tuple(map(int, args.minmax.split(','))), args.floating_precision)

        