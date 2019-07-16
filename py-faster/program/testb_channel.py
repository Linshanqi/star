from __future__ import division
import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import scipy.misc
import csv
import argparse
import sys
def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Train a Faster R-CNN network')
    parser.add_argument('--test-dataset', dest='testdata',
                        help='training dataset',
                        default=None, type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args
def image_upup_by_sitatistic_90percent(filename_a, filename_b, filename_c, filename_out, percent):
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

    scipy.misc.imsave(filename_out, fabc)
args = parse_args()
jpgpath=args.testdata
path1='./data/demo/testB'
star_file = os.path.join(jpgpath,'list.csv')
csv_file=csv.reader(open(star_file,'r'))

if os.path.exists(path1):
    shutil.rmtree(path1)
os.mkdir(path1)
for stu in csv_file:
    if(stu[0]=='id'):
        continue
    print(stu[0])
    a=jpgpath+'/'+stu[0][0:2]+'/'+stu[0]+'_a.jpg'
    b=jpgpath+'/'+stu[0][0:2]+'/'+stu[0]+'_b.jpg'
    c=jpgpath+'/'+stu[0][0:2]+'/'+stu[0]+'_c.jpg'
    d=path1+'/'+stu[0]+'.jpg'
    image_upup_by_sitatistic_90percent(a,b,c,d,1-0.9)
