# -*- coding: utf-8 -*-
from PIL import ImageEnhance
from PIL import Image
import numpy as np
import os
import os.path
from PIL import Image,ImageOps,ImageFilter
import random
from scipy import misc
import glob
import cv2
from math import *
from openpyxl.chart import picture
import shutil
sourcePicture = r'./data/VOCdevkit2007/VOC2007/Images'
augumentPicture = r'./data/VOCdevkit2007/VOC2007/Augumentation'
def getPictureList():
    # set up output dir
    if os.path.exists(augumentPicture): 
        shutil.rmtree(augumentPicture)
    os.mkdir(augumentPicture)
    
    for category in os.listdir(sourcePicture):
        sourceImageList = glob.glob(os.path.join(sourcePicture, '*'))
        for sourceImage in sourceImageList:
            im = Image.open(sourceImage)
            newFileName = os.path.splitext(os.path.basename(sourceImage))[0] + ".jpg"
            picture = os.path.join(augumentPicture,newFileName)
            im.save(os.path.join(augumentPicture,newFileName))        
            flipTransfer(picture)
            remote(picture,90) 
            remote(picture,180) 
            remote(picture,270) 
            
    print("accomplish")  
    
def flipTransfer(picture):
    img = Image.open(picture)
    #img.show()
    x=img.size[0]  
    y=img.size[1] 
    img=img.load()
    c = Image.new("RGB",(x,y))
    d = Image.new("RGB",(x,y))
    
    for i in range (0,x):  
        for j in range (0,y):  
            w=x-i-1  
            h=y-j-1  
            rgb=img[w,j]  
            rgb2 = img[i,h]
            c.putpixel([i,j],rgb)
            d.putpixel([i,j],rgb2)
    #c.show()
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_flip_1.jpg"
    c.save(os.path.join(augumentPicture,newFileName))
    
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_flip_2.jpg"
    d.save(os.path.join(augumentPicture,newFileName))
    
def remote(picture,degree):
    #degree left
    img = cv2.imread(picture)
    height, width = img.shape[:2]
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))

    matRotation = cv2.getRotationMatrix2D((width / 2, height / 2), degree, 1)

    matRotation[0, 2] += (widthNew - width) / 2
    matRotation[1, 2] += (heightNew - height) / 2
    imgRotation = cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))

    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_rotate_"+str(degree)+".jpg"
    cv2.imwrite(os.path.join(augumentPicture,newFileName),imgRotation)

    
     

if __name__ == '__main__':
    getPictureList()