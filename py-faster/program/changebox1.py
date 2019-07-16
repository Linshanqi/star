# -*- coding: utf-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import re
import numpy as np
import os
import os.path
from PIL import Image,ImageOps,ImageFilter
import random
from scipy import misc
import glob


saveDir = './data/VOCdevkit2007/VOC2007/Annotations'


def getXML():
    # set up output dir
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    myNum=0
    sourceXMLList = glob.glob(os.path.join('./data/VOCdevkit2007/VOC2007/Annos', '*'))
    for sourceXML in sourceXMLList:

            doc = xml.dom.minidom.parse(sourceXML)
            x_min=doc.getElementsByTagName('xmin')[0].childNodes[0].data
            x_max=doc.getElementsByTagName('xmax')[0].childNodes[0].data
            y_min=doc.getElementsByTagName('ymin')[0].childNodes[0].data
            y_max=doc.getElementsByTagName('ymax')[0].childNodes[0].data
            myName = "%06d" % myNum
            myNum +=1

            width=int(doc.getElementsByTagName('width')[0].childNodes[0].data)
            height=int(doc.getElementsByTagName('height')[0].childNodes[0].data)
            newFileName = str(myName) + ".xml"
            filename=doc.getElementsByTagName('filename')[0]
            filename.childNodes[0].data=str(myName) + ".jpg"
            f =  open(os.path.join(saveDir,newFileName),  'w',encoding = 'utf-8')
            doc.writexml(f,encoding = 'utf-8')
            f.close()
            
            #filp1
            myName = "%06d" % myNum
            myNum +=1
            newFileName = str(myName) + ".xml"
            filename=doc.getElementsByTagName('filename')[0]
            filename.childNodes[0].data=str(myName) + ".jpg"
            doc.getElementsByTagName('xmin')[0].childNodes[0].data=width-int(x_max)
            doc.getElementsByTagName('xmax')[0].childNodes[0].data=width-int(x_min)
            doc.getElementsByTagName('ymin')[0].childNodes[0].data=y_min
            doc.getElementsByTagName('ymax')[0].childNodes[0].data=y_max
            f =  open(os.path.join(saveDir,newFileName),  'w',encoding = 'utf-8')
            doc.writexml(f,encoding = 'utf-8')
            f.close()
            
                        
            #flip2
            myName = "%06d" % myNum
            myNum +=1
            newFileName = str(myName) + ".xml"
            filename=doc.getElementsByTagName('filename')[0]
            filename.childNodes[0].data=str(myName) + ".jpg"
            doc.getElementsByTagName('xmin')[0].childNodes[0].data=x_min
            doc.getElementsByTagName('xmax')[0].childNodes[0].data=x_max
            doc.getElementsByTagName('ymin')[0].childNodes[0].data=height-int(y_max)
            doc.getElementsByTagName('ymax')[0].childNodes[0].data=height-int(y_min)
            f =  open(os.path.join(saveDir,newFileName),  'w',encoding = 'utf-8')
            doc.writexml(f,encoding = 'utf-8')
            f.close()
            
            #rotate180
            myName = "%06d" % myNum
            myNum +=1
            newFileName = str(myName) + ".xml"
            filename=doc.getElementsByTagName('filename')[0]
            filename.childNodes[0].data=str(myName) + ".jpg"
            doc.getElementsByTagName('xmin')[0].childNodes[0].data=width-int(x_max)
            doc.getElementsByTagName('xmax')[0].childNodes[0].data=width-int(x_min)
            doc.getElementsByTagName('ymin')[0].childNodes[0].data=height-int(y_max)
            doc.getElementsByTagName('ymax')[0].childNodes[0].data=height-int(y_min)
            f =  open(os.path.join(saveDir,newFileName),  'w',encoding = 'utf-8')
            doc.writexml(f,encoding = 'utf-8')
            f.close()
            
            #rotate270
            myName = "%06d" % myNum
            myNum +=1
            newFileName = str(myName) + ".xml"
            filename=doc.getElementsByTagName('filename')[0]
            filename.childNodes[0].data=str(myName) + ".jpg"
            doc.getElementsByTagName('xmin')[0].childNodes[0].data=height-int(y_max)
            doc.getElementsByTagName('xmax')[0].childNodes[0].data=height-int(y_min)
            doc.getElementsByTagName('ymin')[0].childNodes[0].data=x_min
            doc.getElementsByTagName('ymax')[0].childNodes[0].data=x_max
            f =  open(os.path.join(saveDir,newFileName),  'w',encoding = 'utf-8')
            doc.writexml(f,encoding = 'utf-8')
            f.close()
            
            #rotate90
            myName = "%06d" % myNum
            myNum +=1
            newFileName = str(myName) + ".xml"
            filename=doc.getElementsByTagName('filename')[0]
            filename.childNodes[0].data= str(myName)+ ".jpg"
            doc.getElementsByTagName('xmin')[0].childNodes[0].data=y_min
            doc.getElementsByTagName('xmax')[0].childNodes[0].data=y_max
            doc.getElementsByTagName('ymin')[0].childNodes[0].data=width-int(x_max)
            doc.getElementsByTagName('ymax')[0].childNodes[0].data=width-int(x_min)
            f =  open(os.path.join(saveDir,newFileName),  'w',encoding = 'utf-8')
            doc.writexml(f,encoding = 'utf-8')
            f.close()

            
            
if __name__ == '__main__':
    print ('start')
    getXML()
    print ('accomplish')
