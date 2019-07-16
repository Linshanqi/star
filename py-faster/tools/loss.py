#!/usr/bin/env python
import os 
import sys
import numpy as np
import matplotlib.pyplot as plt  
import math  
import re  
import pylab  
from pylab import figure, show, legend  
from mpl_toolkits.axes_grid1 import host_subplot  
      
# read the log file  
fp = open('/home/shelly/py-faster-rcnn/tools/904.txt', 'r')  
      
train_iterations = []  
train_loss = []  
test_iterations = []  
#test_accuracy = []  
      
for ln in fp:  
  # get train_iterations and train_loss  
   if '] Iteration ' in ln and 'loss = ' in ln:  
      arr = re.findall(r'ion \b\d+\b,',ln)  
      train_iterations.append(int(arr[0].strip(',')[4:]))  
      train_loss.append(float(ln.strip().split(' = ')[-1]))  
          
fp.close()  
      
host = host_subplot(111)  
plt.subplots_adjust(right=0.8) # ajust the right boundary of the plot window  
#par1 = host.twinx()  
# set labels  
host.set_xlabel("iterations")  
host.set_ylabel("RPN loss")  
#par1.set_ylabel("validation accuracy")  
      
# plot curves  
p1, = host.plot(train_iterations, train_loss, label="train RPN loss")  
#p2, = par1.plot(test_iterations, test_accuracy, label="validation accuracy")  
      
# set location of the legend,   
# 1->rightup corner, 2->leftup corner, 3->leftdown corner  
# 4->rightdown corner, 5->rightmid ...  
host.legend(loc=1)  
      
# set label color  
host.axis["left"].label.set_color(p1.get_color())  
#par1.axis["right"].label.set_color(p2.get_color())  
# set the range of x axis of host and y axis of par1  
host.set_xlim([0,80000])  
host.set_ylim([0., 1.6])  
      
plt.draw()  
plt.show()  
