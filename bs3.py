""" bs3.py
    Benford Image Statistics
    
    Authors: @gv-sh @bhaumikdebanshu
    License: MIT

    Example:
    >>> python3 bs3.py --dir=data --csv=csv/batch_01.csv --rsz=0.25 --min=0 --max=999 --fp=3
"""

import os
import cv2 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

ls              = lambda dir        : [i for i in os.listdir(dir) if os.path.isfile(os.path.join(dir, i)) and (i.endswith('.jpg') or i.endswith('.jpeg'))]
read            = lambda dir, f     : cv2.imread(os.path.join(dir, f), cv2.IMREAD_GRAYSCALE)
resize          = lambda M, s       : cv2.resize(M, (0, 0), fx=s, fy=s, interpolation=cv2.INTER_AREA)

flatten         = lambda M          : M.flatten()
as_np           = lambda M          : np.array(flatten(M), dtype=np.float16)

norm            = lambda M          : M / M.max()
interp          = lambda M, x, y    : np.interp(M, (M.min(), M.max()), (x, y))

first           = lambda x          : int(str(x)[0])
firsts          = lambda M          : np.array([first(i) for i in M])
count           = lambda M, i       : len([j for j in M if j == i])
counts          = lambda M          : {str(i): count(M, i) for i in range(1, 10)}

prob            = lambda M, i       : M[i] / sum(M.values())
probs           = lambda M          : {str(i): 100*prob(M, str(i)) for i in range(1, 10)}
ben             = lambda            : {str(i): np.log10(1 + 1/i) * 100 for i in range(1, 10)}

write           = lambda D, fp      : pd.DataFrame(D).to_csv(fp, index=False)

log             = lambda msg        : print(msg, end='\r', flush=True)

def bs3(dir, csv, rsz=1, min=0, max=255, fp=8):
    """ Capture Benford Law analysis of all the jpgs/jpegs available in the given directory
    
        @param dir: Directory containing the images 
        @param csv: CSV file to store the results 

        @return None
    """
    files = ls(dir)

    data = []

    index = 0

    for f in files:

        log('Analysing image {}/{}: {}% completed ...'.format(index, len(files), round(100*index/len(files), 2)))

        img     = read(dir, f)
        img_rsz = resize(img, rsz)
        img_np  = as_np(img_rsz)
        img_nrm = norm(img_np)
        img_rmp = interp(img_nrm, min, max)
        img_fst = firsts(img_rmp)
        img_cnt = counts(img_fst)
        img_prb = probs(img_cnt)
        diff = { str(i): round(img_prb[str(i)] - ben()[str(i)], fp) for i in range(1, 10) }

        diff2 = { str(i): pow(diff[str(i)], 2) for i in range(1, 10) }
        sum_diff2 = sum(diff2.values())

        for i in range(1, 10):

            data.append({
                'dir'   : dir,
                'ref'   : f, 
                'min'   : min,
                'max'   : max,
                'rsz'   : rsz,
                'fp'    : fp,
                'w'     : img.shape[1],
                'h'     : img.shape[0],
                'dig'   : i,
                'cnt'   : img_cnt[str(i)],
                'prb'   : round(img_prb[str(i)], fp),
                'ben'   : round(ben()[str(i)], fp),
                'diff'  : diff[str(i)],
                'diff2' : diff2[str(i)],
                'sum_diff2' : sum_diff2
            }
        )

        index += 1

    write(data, csv)
    log('Processed {} images and stored the results in {}'.format(len(files), csv))

def preview(img, cmap='gray'):
    """ Display the image 
    
        @param img: Image to display

        @return None
    """
    plt.imshow(img, cmap=cmap)    
    plt.show()

def image_grid(imgs, rows, cols, figsize=(10, 10), cmap='gray'):
    """ Display a grid of images 
    
        @param imgs: List of images to display
        @param rows: Number of rows in the grid
        @param cols: Number of columns in the grid
        @param figsize: Size of the figure

        @return None
    """
    fig, axs = plt.subplots(rows, cols, figsize=figsize)
    fig.tight_layout()

    for i in range(rows):
        for j in range(cols):
            axs[i, j].imshow(imgs[i * cols + j], cmap=cmap)
            axs[i, j].set_title('Image {}'.format(i * cols + j + 1))

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Benford Image Statistics')
    parser.add_argument('-d', '--dir', type=str     , help='Directory containing the images', required=True)
    parser.add_argument('-c', '--csv', type=str     , help='CSV file to store the results'  , required=True)
    parser.add_argument('-r', '--rsz', type=float   , help='Resize factor'                  , default=1)
    parser.add_argument('-m', '--min', type=int     , help='Minimum pixel value'            , default=0)
    parser.add_argument('-M', '--max', type=int     , help='Maximum pixel value'            , default=255)
    parser.add_argument('-f', '--fp' , type=int     , help='Floating precision'             , default=8)
    args = parser.parse_args()

    bs3(args.dir, args.csv, args.rsz, args.min, args.max, args.fp)