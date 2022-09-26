import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

load_image_files    = lambda dir    : [f for f in os.listdir(dir) if f.endswith('.jpg') or f.endswith('.jpeg')]
read_images         = lambda dir, F : [cv2.imread(os.path.join(dir, f)) for f in F]

grayscale           = lambda I      : cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
rgb                 = lambda I      : cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
hsv                 = lambda I      : cv2.cvtColor(I, cv2.COLOR_BGR2HSV)

red                 = lambda I      : rgb(I)[:,:,0].flatten()
green               = lambda I      : rgb(I)[:,:,1].flatten()
blue                = lambda I      : rgb(I)[:,:,2].flatten()
gray                = lambda I      : grayscale(I).flatten()
hue                 = lambda I      : hsv(I)[:,:,0].flatten()
sat                 = lambda I      : hsv(I)[:,:,1].flatten()
val                 = lambda I      : hsv(I)[:,:,2].flatten()

first               = lambda x      : int(str(x)[0])
firsts              = lambda A      : [first(x) for x in A]
benford             = lambda A      : [A.count(x) for x in range(1,10)]
benford_pct         = lambda A      : [x/sum(A) for x in benford(A)]

