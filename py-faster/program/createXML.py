import os
import sys

from PIL import Image
from itertools import islice
from xml.dom.minidom import Document
import shutil

labels=r'./data/VOCdevkit2007/VOC2007/Labels'
imgpath=r'./data/VOCdevkit2007/VOC2007/JPEGImages'

xmlpath_new=r'./data/VOCdevkit2007/VOC2007/Annotations'
foldername='VOC2007'
prePic=r'./data/VOCdevkit2007/VOC2007/jpg90percent'

def insertObject(doc,i, L):
    obj = doc.createElement('object')
    content=doc.createElement('content')
    content.appendChild(doc.createTextNode(str(L[i][0])))
    obj.appendChild(content)
    name = doc.createElement('name')
    name.appendChild(doc.createTextNode(str(L[i][0])))
    obj.appendChild(name)
    pose = doc.createElement('pose')
    pose.appendChild(doc.createTextNode('Unspecified'))
    obj.appendChild(pose)
    truncated = doc.createElement('truncated')
    truncated.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(truncated)
    difficult = doc.createElement('difficult')
    difficult.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(difficult)
    bndbox = doc.createElement('bndbox')
    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode(str(L[i][1])))
    bndbox.appendChild(xmin)
        
    ymin = doc.createElement('ymin')                
    ymin.appendChild(doc.createTextNode(str(L[i][2])))
    bndbox.appendChild(ymin)                
    xmax = doc.createElement('xmax')                
    xmax.appendChild(doc.createTextNode(str(L[i][3])))
    bndbox.appendChild(xmax)                
    ymax = doc.createElement('ymax')    
    if  '\r' == str(L[i][4])[-1] or '\n' == str(L[i][4])[-1]:
        data = str(L[i][4])[0:-1]
    else:
        data = str(L[i][4])
    ymax.appendChild(doc.createTextNode(data))
    bndbox.appendChild(ymax)
    obj.appendChild(bndbox)                    
    return obj

def create():
    if  os.path.exists(imgpath):
        shutil.rmtree(imgpath)
    if  os.path.exists(xmlpath_new):
        shutil.rmtree(xmlpath_new)
    os.mkdir(os.path.join(imgpath))
    os.mkdir(os.path.join(xmlpath_new))
    num=0
    for category in os.listdir(labels):
        L=[]
        M=[]
        indexNum=os.path.splitext(os.path.basename(category))[0]
        pictureName = category.replace('.txt', '.jpg')
        # originName=os.path.join(originPic,str(indexNum)+"_d.jpg")
        preName=os.path.join(prePic,str(indexNum)+".jpg")
        indexName = "%06d" % num
        picturePathIndexName = os.path.join(imgpath,indexName+".jpg")
        shutil.copy(preName,picturePathIndexName)
        fidin=open(labels + '/'+ category,'r',encoding="utf-8")
        for data in islice(fidin, 1, None):        
            data=data.strip('\n')
            con=data.split(' ')

            print(con)
            L.append(con)
        img = Image.open(picturePathIndexName)
        imgSize = img.size
        imgSize = imgSize + (3,)

        f = open(os.path.join(xmlpath_new,indexName+".xml"), "w")
        doc= Document()
        annotation = doc.createElement('annotation')
        doc.appendChild(annotation)
                        
        folder = doc.createElement('folder')
        folder.appendChild(doc.createTextNode(foldername))
        annotation.appendChild(folder)
                        
        filename = doc.createElement('filename')
        filename.appendChild(doc.createTextNode(indexName+".jpg"))
        annotation.appendChild(filename)
                        
        source = doc.createElement('source')                
        database = doc.createElement('database')
        database.appendChild(doc.createTextNode('My Database'))
        source.appendChild(database)
        source_annotation = doc.createElement('annotation')
        source_annotation.appendChild(doc.createTextNode(foldername))
        source.appendChild(source_annotation)
        image = doc.createElement('image')
        image.appendChild(doc.createTextNode('flickr'))
        source.appendChild(image)
        flickrid = doc.createElement('flickrid')
        flickrid.appendChild(doc.createTextNode('NULL'))
        source.appendChild(flickrid)
        annotation.appendChild(source)
                        
        owner = doc.createElement('owner')
        flickrid = doc.createElement('flickrid')
        flickrid.appendChild(doc.createTextNode('NULL'))
        owner.appendChild(flickrid)
        name = doc.createElement('name')
        name.appendChild(doc.createTextNode('idaneel'))
        owner.appendChild(name)
        annotation.appendChild(owner)
                        
        size = doc.createElement('size')
        width = doc.createElement('width')
        width.appendChild(doc.createTextNode(str(imgSize[0])))
        size.appendChild(width)
        height = doc.createElement('height')
        height.appendChild(doc.createTextNode(str(imgSize[1])))
        size.appendChild(height)
        depth = doc.createElement('depth')
        depth.appendChild(doc.createTextNode(str(imgSize[2])))
        size.appendChild(depth)
        annotation.appendChild(size)
                        
        segmented = doc.createElement('segmented')
        segmented.appendChild(doc.createTextNode(str(0)))
        annotation.appendChild(segmented)
        for i in range(len(L)):            
            annotation.appendChild(insertObject(doc,i, L))
        try:
            f.write(doc.toprettyxml(indent = '    '))
            f.close()
            fidin.close()
        except:
            pass
        num=num+1
if __name__ == '__main__':
    create()