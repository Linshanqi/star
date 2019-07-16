import os
import csv
import sys,operator
import random

from operator import itemgetter
originPath='./top3/result.txt'
sortPath='./top3/sort.txt'

resultPath='./top3/submit.txt'
inopen=open(originPath, 'r+')
lines=inopen.readlines()
result=[]
for line in lines:
	result.append(line)
result.sort()
if os.path.exists(sortPath):
	os.remove(sortPath)
if os.path.exists(resultPath):
	os.remove(resultPath)

outopen=open(sortPath, 'w')
outfopen=open(resultPath,'w')
L=[]	
for s in result:
	ss=s.split(' ')
	L.append(ss)
	stu=ss[0]+' '+ss[1]+' '+str(ss[2])+' '+str(ss[3])+' '+str(ss[4])+' '+str(ss[5])+' '+str(ss[6])
	outopen.write(stu)
i=0
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
	if(count==1):
		outfopen.write(M[0][0]+' '+str(M[0][1])+' '+str(M[0][2])+' '+str(M[0][4])+' '+str(M[0][5])+' '+str(M[0][6])+' '+str(M[0][7])+' '+str(random.randint(0,1))+'\n')
	elif(count==2):
		N=sorted(M, key=itemgetter(3), reverse=True)
		outfopen.write(N[0][0]+' '+str(N[0][1])+' '+str(N[0][2])+' '+str(N[1][1])+' '+str(N[1][2])+' '+str(N[0][4])+' '+str(N[0][5])+' '+str(random.randint(0,1))+'\n')
	elif(count>=3):
		N=sorted(M, key=itemgetter(3), reverse=True)
		outfopen.write(N[0][0]+' '+str(N[0][1])+' '+str(N[0][2])+' '+str(N[1][1])+' '+str(N[1][2])+' '+str(N[2][1])+' '+str(N[2][2])+' '+str(random.randint(0,1))+'\n')
	i=j
inopen.close()
outfopen.close()
outopen.close()	