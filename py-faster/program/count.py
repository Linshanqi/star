import os
import csv
import sys,operator
import random
# from itertools import groupby
from operator import itemgetter
# originPath='/home/shelly/py-faster-rcnn/result_90/result_90.txt'
sortPath='./sort.txt'

resultPath='./count.txt'
# inopen=open(originPath, 'r+')
# lines=inopen.readlines()
# result=[]
# for line in lines:
# 	result.append(line)
# result.sort()
# if os.path.exists(sortPath):
# 	os.remove(sortPath)
# if os.path.exists(resultPath):
# 	os.remove(resultPath)
# if os.path.exists(csvPath):
# 	os.remove(csvPath)
outopen=open(sortPath, 'r+')
lines=outopen.readlines()
L=[]
for line in lines:
	line=line.split(' ')
	L.append(line)
outfopen=open(resultPath,'w')
# L=[]	
# for s in result:
# 	# print(s)
# 	ss=s.split(' ')
# 	L.append(ss)
# 	stu=ss[0]+' '+ss[1]+' '+str(ss[2])+' '+str(ss[3])+' '+str(ss[4])+' '+str(ss[5])+' '+str(ss[6])
# 	outopen.write(stu)
i=0
c=1
while i <len(L):
	count=1
	j=i+1
	M=[]
	idname=os.path.splitext(os.path.basename(L[i][0]))[0]
	x1=(int(L[i][2])+int(L[i][4]))//2
	y1=(int(L[i][3])+int(L[i][5]))//2
	coor=[idname,x1,y1,L[i][6],L[i][2],L[i][3],L[i][4],L[i][5]]
	M.append(coor)
	# outfopen.write(idname+' '+x1+' '+y1+' ')
	while  j<=len(L)-1 and L[j][0]==L[i][0]:
		# if(count<=3):
		# 	# x=
		# 	outfopen.write(L[j][2]+' '+L[j][3]+' '+L[j][4]+' '+L[j][5]+' ')
		x=(int(L[j][2])+int(L[j][4]))//2
		y=(int(L[j][3])+int(L[j][5]))//2
		coor1=[idname,x,y,L[j][6],L[j][2],L[j][3],L[j][4],L[j][5]]
		M.append(coor1)
		count=count+1
		j=j+1
	# outfopen.write(M[j-1][0]+' '+str(count)+'\n')
	if(count<=2):
		c=c+1

	i=j
print(c)
outfopen.close()
outopen.close()		