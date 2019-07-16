from __future__ import division
import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import scipy.misc
import csv
import shutil
import argparse
import sys
# def parse_args():
#     """
#     Parse input arguments
#     """
#     parser = argparse.ArgumentParser(description='Train a Faster R-CNN network')
#     parser.add_argument('--training-dataset', dest='traindata',
#                         help='training dataset',
#                         default=None, type=str)

#     if len(sys.argv) == 1:
#         parser.print_help()
#         sys.exit(1)

#     args = parser.parse_args()
#     return args
def image_upup_by_sitatistic_90percent(filename_a, filename_b, filename_c, filename_out, filename_out1,filename_out2,filename_out3,percent):
    fa = np.array(mpimg.imread(filename_a))
    fb = np.array(mpimg.imread(filename_b))
    fc = np.array(mpimg.imread(filename_c))
    all = fa.size
    i=0
    for i in range(10,255,1):
        fa[fa<i]=0
        count = np.count_nonzero(fa)
        r = count/all
        # print("r:"+str(r))
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

    scipy.misc.imsave(filename_out1, fa)
    scipy.misc.imsave(filename_out2, fb)
    scipy.misc.imsave(filename_out3, fc)
    scipy.misc.imsave(filename_out, fabc)

# args = parse_args()
# jpgpath=args.traindata

jpgpath=r'./data'
# star_file=os.path.join(jpgpath,'list.csv')
# star_file = r'./data/VOCdevkit2007/VOC2007/af2019-cv-training-20190312/list.csv'
# csv_file=csv.reader(open(star_file,'r'))
# if os.path.exists(path1):
#     shutil.rmtree(path1)
# os.mkdir(path1)
# for stu in csv_file:
    # if(stu[0]=='id'):
        # continue
    # print(stu[0])
    # print(stu[0])
    # if(stu[3]!='pity'):
a=jpgpath+'/0af6e4acd1cddf76c5378d20e3bfcb9f_a.jpg'
b=jpgpath+'/0af6e4acd1cddf76c5378d20e3bfcb9f_b.jpg'
c=jpgpath+'/0af6e4acd1cddf76c5378d20e3bfcb9f_c.jpg'
d=jpgpath+'/0af6e4acd1cddf76c5378d20e3bfcb9f.jpg'
e=jpgpath+'/0af6e4acd1cddf76c5378d20e3bfcb9f_a1.jpg'
f=jpgpath+'/0af6e4acd1cddf76c5378d20e3bfcb9f_b1.jpg'
g=jpgpath+'/0af6e4acd1cddf76c5378d20e3bfcb9f_c1.jpg'
image_upup_by_sitatistic_90percent(a,b,c,d,e,f,g,1-0.9)