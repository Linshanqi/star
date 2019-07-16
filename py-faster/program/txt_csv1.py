import csv

resultPath='./pity/submit.txt'
txtPath='./data/demo/list.csv'

csv_file = csv.reader(open(txtPath,'r'))
L=[]
with open(resultPath, 'r+',encoding="utf-8") as ffopen:
	lines=ffopen.readlines()
with open(resultPath, 'a+',encoding="utf-8") as outfopen:
	for line in lines:
		a=line.split(' ')
		L.append(a[0])
	for stu in csv_file:
		if (stu[0]=='id'):
			continue
		if stu[0] not in L:
			str1=stu[0]+' '+'0'+' '+'0'+' '+'0'+' '+'0'+' '+'0'+' '+'0'+' '+'0'+'\n'
			outfopen.write(str1)


with open(resultPath, 'r+',encoding="utf-8") as infopen:
	liness = infopen.readlines()
	fw=open('./pity/submit.csv','a',newline='')
	csv_write=csv.writer(fw,dialect='excel')
	head=['id','x1','y1','x2','y2','x3','y3','havestar']
	csv_write.writerow(head)
	for line in liness:
		ss=line.split(' ')
		
		stu=[ss[0],int(ss[1]),int(ss[2]),int(ss[3]),int(ss[4]),int(ss[5]),int(ss[6]),int(ss[7])]
		
		csv_write.writerow(stu)

