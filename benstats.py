""" benstats.py
    Benford Image Statistics
    
    Authors: @gv-sh @bhaumikdebanshu
    License: MIT

    Example:
    >>> python3 benstats.py --dir=data --csv=batch.csv
"""

import os
import pandas as pd
import PIL.Image as Image
import PIL.ImageStat as stat
import argparse

float_precision     = 12

first               = lambda x      : int(str(x)[0])
firsts              = lambda A      : [first(x) for x in A]
benford             = lambda A      : [firsts(A).count(x) for x in range(1,10)]
benford_pct         = lambda A      : [round(x/sum(A), float_precision) for x in benford(A)]

def benstats(dir, csv, info = False, exif = False):
    """ Capture Benford Law analysis of all the jpgs/jpegs available in the given directory
    
        @param dir: Directory containing the images 
        @param csv: CSV file to store the results 

        @return None
    """

    # List of all the jpgs/jpegs in the given directory
    files = [f for f in os.listdir(dir) if f.endswith('.jpg') or f.endswith('.jpeg')]

    print("Found {} images in the given directory".format(len(files)))

    batch = []

    # Iterate over all the jpgs/jpegs and capture the Benford Law analysis
    for f in files:

        data = {}

        print("Image {} of {} - (1/4) Reading: {}".format(files.index(f)+1, len(files), f), end='\r')

        # Read the image using PIL
        img = Image.open(os.path.join(dir, f))

        print("Image {} of {} - (1/4) Reading: Basic info..                                     ".format(files.index(f)+1, len(files)), end='\r')

        # Basic information
        data['source_dir'] = dir
        data['source_filename'] = f
        data['format'] = img.format
        data['color_mode'] = img.mode
        data['width'] = img.width
        data['height'] = img.height

        if info:
            if img.info:
                for k, v in img.info.items():
                    data["info_" + str(k)] = v

        if exif:
            print("Image {} of {} - (1/4) Reading: EXIF data..                                  ".format(files.index(f)+1, len(files)), end='\r')

            # Image EXIF data
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    data["exif_" + str(tag)] = value

        print("Image {} of {} - (2/4) Computing: Pixel stats..                                  ".format(files.index(f)+1, len(files)), end='\r')

        # Image statistics
        data['pixel_extrema_red_min'] = stat.Stat(img).extrema[0][0]
        data['pixel_extrema_red_max'] = stat.Stat(img).extrema[0][1]
        data['pixel_extrema_green_min'] = stat.Stat(img).extrema[1][0]
        data['pixel_extrema_green_max'] = stat.Stat(img).extrema[1][1]
        data['pixel_extrema_blue_min'] = stat.Stat(img).extrema[2][0]
        data['pixel_extrema_blue_max'] = stat.Stat(img).extrema[2][1]

        data['pixel_count_red'] = stat.Stat(img).count[0]
        data['pixel_count_green'] = stat.Stat(img).count[1]
        data['pixel_count_blue'] = stat.Stat(img).count[2]

        data['pixel_sum_red'] = stat.Stat(img).sum[0]
        data['pixel_sum_green'] = stat.Stat(img).sum[1]
        data['pixel_sum_blue'] = stat.Stat(img).sum[2]

        data['pixel_sum2_red'] = stat.Stat(img).sum2[0]
        data['pixel_sum2_green'] = stat.Stat(img).sum2[1]
        data['pixel_sum2_blue'] = stat.Stat(img).sum2[2]

        data['pixel_mean_red'] = stat.Stat(img).mean[0]
        data['pixel_mean_green'] = stat.Stat(img).mean[1]
        data['pixel_mean_blue'] = stat.Stat(img).mean[2]

        data['pixel_median_red'] = stat.Stat(img).median[0]
        data['pixel_median_green'] = stat.Stat(img).median[1]
        data['pixel_median_blue'] = stat.Stat(img).median[2]

        data['pixel_rms_red'] = stat.Stat(img).rms[0]
        data['pixel_rms_green'] = stat.Stat(img).rms[1]
        data['pixel_rms_blue'] = stat.Stat(img).rms[2]

        data['pixel_var_red'] = stat.Stat(img).var[0]
        data['pixel_var_green'] = stat.Stat(img).var[1]
        data['pixel_var_blue'] = stat.Stat(img).var[2]

        data['pixel_stddev_red'] = stat.Stat(img).stddev[0]
        data['pixel_stddev_green'] = stat.Stat(img).stddev[1]
        data['pixel_stddev_blue'] = stat.Stat(img).stddev[2]

        print("Image {} of {} - (3/4) Benford: Splitting RGB channels..                         ".format(files.index(f)+1, len(files)), end='\r')

        # Get RGB values
        r, g, b = img.split()

        print("Image {} of {} - (3/4) Benford: Analysing Red channel..                          ".format(files.index(f)+1, len(files)), end='\r')

        red = benford_pct(list(r.getdata()))

        for i in range(1, 10):
            data['red_' + str(i)] = red[i-1]

        print("Image {} of {} - (3/4) Benford: Analysing Green channel..                        ".format(files.index(f)+1, len(files)), end='\r')
        
        green = benford_pct(list(g.getdata()))

        for i in range(1, 10):
            data['green_' + str(i)] = green[i-1]

        print("Image {} of {} - (3/4) Benford: Analysing Blue channel..                         ".format(files.index(f)+1, len(files)), end='\r')

        blue = benford_pct(list(b.getdata()))
        
        for i in range(1, 10):
            data['blue_' + str(i)] = blue[i-1]

        print("Image {} of {} - (3/4) Benford: Converting image into Grayscale..                ".format(files.index(f)+1, len(files)), end='\r')

        # Convert image to grayscale
        img = img.convert('L')

        print("Image {} of {} - (3/4) Benford: Analysing Gray channel..                         ".format(files.index(f)+1, len(files)), end='\r')

        gray = benford_pct(list(img.getdata()))

        for i in range(1, 10):
            data['gray_' + str(i)] = gray[i-1]

        # Close PIL image
        img.close()

        print("Image {} of {}: (4/4) Collecting stats..                                         ".format(files.index(f)+1, len(files)), end='\r')

        # Append data to batch
        batch.append(data)

    print("Creating dataframe..")

    # Create dataframe using batch 
    df = pd.DataFrame(batch)

    print("Saving dataframe to CSV..")

    # Save dataframe to CSV
    df.to_csv(csv, index=False)

    print("Saved CSV to {}".format(csv))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Benford Image Statistics')
    parser.add_argument('-d', '--dir', help='Directory containing the images', required=True)
    parser.add_argument('-c', '--csv', help='CSV file to store the results', required=True)
    parser.add_argument('-e', '--exif', help='Capture EXIF data', action='store_true')
    parser.add_argument('-i', '--info', help='Capture Info', action="store_true")

    args = parser.parse_args()

    benstats(args.dir, args.csv, args.exif, args.info)



