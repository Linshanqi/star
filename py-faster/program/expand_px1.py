import csv
import os
import shutil
from PIL import Image
import argparse
import sys

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Train a Fast R-CNN network')
    parser.add_argument('--training-dataset', dest='traindata',
                        help='training dataset',
                        default=None, type=str)


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

args = parse_args()
star = args.traindata
star_file=os.path.join(star,'list.csv')
path=r'./data/VOCdevkit2007/VOC2007/Labels'
originPic=r'./data/VOCdevkit2007/VOC2007/jpg90percent'
csv_file=csv.reader(open(star_file,'r'))
print(csv_file)
if os.path.exists(path):
	shutil.rmtree(path)

os.mkdir(path)

for stu in csv_file:
	if(stu[0]=='id'):
		continue
	ss=stu[0]+'.jpg'
	sss=os.path.join(originPic,ss)
	im=Image.open(sss)
	imSize = im.size
	imSize = imSize + (3,)
	imwidth=imSize[0]
	imheight=imSize[1]
	if(int(stu[1])>imwidth or int(stu[2])>imheight):
		print(stu[0]+'error')
		continue
	x1=int(stu[1])-15
	x2=int(stu[1])+15
	y1=int(stu[2])-15
	y2=int(stu[2])+15
	if(x1<0):
		x1=0
	if(y1<0):
		y1=0
	if(x2>imwidth):
		x2=imwidth
	if(y2>imheight):
		y2=imheight
	aa=x2-x1
	bb=y2-y1
	L=['newtarget','isstar','asteroid','isnova','known']
	if stu[3] in L:
		label='star'
	else:
		label='noise'
	filename=os.path.join(path,stu[0]+'.txt')
	outfopen = open(filename, 'w',encoding="utf-8")
	line2='1'+'\n'
	line1=line2+label+' '+str(x1)+' '+str(y1)+' '+str(x2)+ ' '+str(y2)
	outfopen.write(line1)
	outfopen.close()
