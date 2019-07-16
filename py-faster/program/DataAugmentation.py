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
from itertools import islice
sourcePicture = r'./data/VOCdevkit2007/VOC2007/11'
augumentPicture = r'./data/VOCdevkit2007/VOC2007/22'
sourceLabel= r'./data/VOCdevkit2007/VOC2007/Labels'
augmentLabel= r'./data/VOCdevkit2007/VOC2007/Label11'

def getPictureList():
    # set up output dir
    if os.path.exists(augumentPicture): 
        shutil.rmtree(augumentPicture)
    os.mkdir(augumentPicture)
    if os.path.exists(augmentLabel): 
        shutil.rmtree(augmentLabel)
    os.mkdir(augmentLabel)
    for category in os.listdir(sourcePicture):
        sourceImageList = glob.glob(os.path.join(sourcePicture, '*'))
        for sourceImage in sourceImageList:
            L=[]
            im = Image.open(sourceImage)
            Labelname=os.path.splitext(os.path.basename(sourceImage))[0] + ".txt"
            label=os.path.join(sourceLabel,Labelname)
            label1=os.path.join(augmentLabel,Labelname)
            shutil.copy(label,label1)
            ffopen=open(label,'r+')
            for data in islice(ffopen, 1, None):
                data=data.strip('\n')
                con=data.split(' ')
                L.append(con)
            print(con)
            imSize = im.size
            imSize = imSize + (3,)
            imwidth=imSize[0]
            imheight=imSize[1]
            newFileName = os.path.splitext(os.path.basename(sourceImage))[0] + ".jpg"
            picture = os.path.join(augumentPicture,newFileName)
            im.save(os.path.join(augumentPicture,newFileName))        
            flipTransfer(picture,L,imwidth,imheight)
            remote(picture,90,L,imwidth,imheight) 
            remote(picture,180,L,imwidth,imheight) 
            remote(picture,270,L,imwidth,imheight) 
            
    print("accomplish")  
    
def flipTransfer(picture,L,imwidth,imheight):
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
    newLabelNames1= os.path.splitext(os.path.basename(picture))[0] + "_flip_1"+".txt"
    newLabelName1=os.path.join(augmentLabel,newLabelNames1)
    fopen=open(newLabelName1,'w')
    str1='1'+'\n'
    x1=imwidth-int(L[0][3])
    x2=imwidth-int(L[0][1])
    y1=L[0][2]
    y2=L[0][4]
    str2='star'+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)
    str3=str1+str2
    fopen.write(str3)
    fopen.close()
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_flip_2.jpg"
    d.save(os.path.join(augumentPicture,newFileName))
    newLabelNames2= os.path.splitext(os.path.basename(picture))[0] + "_flip_1"+".txt"
    newLabelName2=os.path.join(augmentLabel,newLabelNames2)
    ffopen=open(newLabelName2,'w')
    str1='1'+'\n'
    x1=L[0][1]
    x2=L[0][3]
    y1=imheight-int(L[0][4])
    y2=imheight-int(L[0][2])
    str2='star'+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)
    str3=str1+str2
    ffopen.write(str3)
    ffopen.close()
    
def remote(picture,degree,L,imwidth,imheight):
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
    newLabelNames3= os.path.splitext(os.path.basename(picture))[0] + "_rotate_"+str(degree)+".txt"
    newLabelName=os.path.join(augmentLabel,newLabelNames3)
    if(degree==90):
        fopen=open(newLabelName,'w')
        str1='1'+'\n'
        x1=L[0][2]
        x2=L[0][4]
        y1=imwidth-int(L[0][3])
        y2=imwidth-int(L[0][1])
        str2='star'+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)
        str3=str1+str2
        fopen.write(str3)
        fopen.close()
    elif(degree==180):
        fopen=open(newLabelName,'w')
        str1='1'+'\n'
        x1=imwidth-int(L[0][3])
        x2=imwidth-int(L[0][1])
        y1=imheight-int(L[0][4])
        y2=imheight-int(L[0][2])
        str2='star'+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)
        str3=str1+str2
        fopen.write(str3)
        fopen.close()
    elif(degree==270):
        fopen=open(newLabelName,'w')
        str1='1'+'\n'
        x1=imheight-int(L[0][4])
        x2=imheight-int(L[0][2])
        y1=L[0][1]
        y2=L[0][3]
        str2='star'+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)
        str3=str1+str2
        fopen.write(str3)
        fopen.close()
    
     

if __name__ == '__main__':
    getPictureList()