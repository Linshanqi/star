path1=./trial_resnet.txt
path2=./trial_vgg.txt
ffopen=open(path1,'r+')
fopen=open(path2,'a')
lines=ffopen.readlines()
for line in lines:
	fopen.write(line)