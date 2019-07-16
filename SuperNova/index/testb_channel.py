from __future__ import division
import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import scipy.misc
import csv
import argparse
import sys

def image_upup_by_sitatistic_90percent(filename_a, filename_b, filename_c, percent):
    fa = np.array(mpimg.imread(filename_a))
    fb = np.array(mpimg.imread(filename_b))
    fc = np.array(mpimg.imread(filename_c))
    all = fa.size
    i=0
    for i in range(10,255,1):
        fa[fa<i]=0
        count = np.count_nonzero(fa)
        r = count/all
        print("r:"+str(r))
        if(r<percent):
            break
            
    print("fa:"+str(i))
    
    for i in range(10, 255, 1):
        fb[fb < i] = 0
        count = np.count_nonzero(fb)
        
        if (count / all < percent):
            break

    print("fb:" + str(i))
    
    for i in range(10, 255, 1):
        fc[fc < i] = 0
        count = np.count_nonzero(fc)
        if (count / all <percent):
            break

    print("fc:" + str(i))

    DMIX, DMIY = fa.shape
    fabc = np.ones((DMIX, DMIY, 3), dtype='int16')
    for i in range(DMIX):
        for j in range(DMIY):
            fabc[i][j][0] = fa[i][j]
            fabc[i][j][1] = fb[i][j]
            fabc[i][j][2] = fc[i][j]

    scipy.misc.imsave('/home/shelly/flask/star/star/SuperNova/index/static/test4.jpg', fabc)