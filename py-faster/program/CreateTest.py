# -*- coding: utf-8 -*-
import os
import sys
import random
import shutil

try:
    start = 1
    end = 6288
    test1 = 628
    test2 = 628
    allNum = 6288
except:
    print ('Please input picture range')
    print ('./createTest.py 1 1500 500')
    os._exit(0)

b_list = range(start,end)
blist_webId = random.sample(b_list, test1)
blist_webId = sorted(blist_webId)
allFile=[]
M=[]
imageSetsdir = r'./data/VOCdevkit2007/VOC2007/ImageSets'
if  os.path.exists(imageSetsdir):
    shutil.rmtree(imageSetsdir)
os.mkdir(imageSetsdir)

maindir = os.path.join(imageSetsdir,"Main")
if  os.path.exists(maindir):
    shutil.rmtree(maindir)
os.mkdir(maindir)

testFile = open('./data/VOCdevkit2007/VOC2007/ImageSets/Main/test.txt', 'w')
trainvalFile = open('./data/VOCdevkit2007/VOC2007/ImageSets/Main/trainval.txt', 'w')
trainFile = open('./data/VOCdevkit2007/VOC2007/ImageSets/Main/train.txt', 'w')
valFile = open('./data/VOCdevkit2007/VOC2007/ImageSets/Main/val.txt', 'w')

for i in range(allNum):
    allFile.append(i+1)

for test in blist_webId:
    allFile.remove(test)
    testFile.write("%06d" % (test-1) + '\n')
for trainval in allFile:
    M.append(trainval)
    trainvalFile.write("%06d" % (trainval-1) + '\n')
    
clist_webId = random.sample(allFile,test2)
clist_webId = sorted(clist_webId)   

for val in clist_webId:
    M.remove(val)   
    valFile.write("%06d" % (val-1) + '\n')
for train in M:
    # M.remove(train)
    trainFile.write("%06d" % (train-1) + '\n')  
testFile.close()
trainvalFile.close()
trainFile.close()
valFile.close()
