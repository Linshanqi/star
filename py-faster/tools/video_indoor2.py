#!/usr/bin/env python
# coding: utf-8
 
# --------------------------------------------------------
# Object Detection in Video with Faster R-CNN
# Written by Masahiro Rikiso @ 2016/7/20
# --------------------------------------------------------
 
 

 
 
### Set Up Paths for Fast R-CNN
import os
import sys
# Add caffe to PYTHONPATH
caffe_path = os.path.join('/home','shelly','py-faster-rcnn', 'caffe-fast-rcnn', 'python')
sys.path.insert(0, caffe_path)
# Add lib to PYTHONPATH
lib_path = os.path.join('/home','shelly','py-faster-rcnn', 'lib')
sys.path.insert(0, lib_path)
 
 
### Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2
import caffe
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import numpy as np
import matplotlib.pyplot as plt
import threading 
import copy
 
### Define Object-Detection-Function
### Config
global INPUT_FILE
global OUTPUT_FILE
global CONF_THRESH
global NMS_THRESH
global CLASSES
global NETS
INPUT_FILE = "/home/shelly/2.mp4"
OUTPUT_FILE = '/home/shelly/ob4.avi'
CONF_THRESH = 0.5
NMS_THRESH = 0.001

CLASSES = ('__background__',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')
 
NETS = {'vgg16': ('VGG16',
                  'VGG16_faster_rcnn_final.caffemodel'),
        'zf': ('ZF',
                  'ZF_faster_rcnn_final.caffemodel')}
 
def obj_detect(net, im):
    """Detect object classes in an image using pre-computed object proposals."""
 
    # Detect all object classes and regress object bounds
    scores, boxes = im_detect(net, im)
    #im = im[:, :, (2, 1, 0)]
    # Visualize detections for each class
    # CONF_THRESH = 0.1
    # NMS_THRESH = 0.3
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        im = vis_detections(str(cls_ind), im, cls, dets, thresh=CONF_THRESH)

    return im


def obj_track(frame):
    global roi_hist
    global boundingBox
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
    tempBoundingBox = []
    while(len(boundingBox) > 0):
        tempList = boundingBox.pop(0)
        x1 = tempList[0]
        y1 = tempList[1]
        x2 = tempList[2]
        y2 = tempList[3]
        track_window = (x1,y1,x2-x1,y2-y1)
        #track_window = tuple(boundingBox.pop(0))
        print track_window
        # 调用meanshift获取新的位置
        #ret,track_window = cv2.meanShift(dst,track_window,term_crit)
        ret,track_window = cv2.CamShift(dst,track_window,term_crit)
        print "track_window2"
        print track_window
        # 画出它的位置
        #x1,y1,x2-x1,y2-y1 = track_window
        tempList[0] = track_window[0]
        tempList[1] = track_window[1]
        tempList[2] = track_window[0] + track_window[2]
        tempList[3] = track_window[1] + track_window[3]
        tempBoundingBox.append(tempList)
        cv2.rectangle(frame,(tempList[0],tempList[1]),(tempList[2],tempList[3]),255,2)
        #cv2.imshow("frame",frame)
    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#RBG到HSV颜色空间转换
    #print hsv_roi
    mask = cv2.inRange(hsv_roi, np.array((0.,0.,32.)), np.array((180.,255.,255.)))
    roi_hist = cv2.calcHist([hsv_roi],[0],None,[180],[0,180 ])
    #---------------------传入图像，灰度图像[0]，统计整张图None，灰度级个数，像素值范围
    #plt.plot(roi_hist)
    #plt.show()
    #cv2.waitKey(0)
    cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
    #------------输入数组，输出数组，模式最小值，最大值，数组数值平移或缩放到某一个范围
    #plt.plot(roi_hist)
    #plt.show()
    boundingBox = copy.deepcopy(tempBoundingBox)
    return frame
 
def vis_detections(image_name, im, class_name, dets, thresh=0.5):
    global boundingBox
    global nextBoundingBox
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return im
    boundingBox = copy.deepcopy(nextBoundingBox)
    nextBoundingBox=[] 
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
        nextBoundingBox.append(bbox)
        if (bbox[2] - bbox[0]) < 352 and (bbox[3] - bbox[1]) < 240:
            #cv2.putText(im, '{:s} {:.3f}'.format(class_name, score),(int(bbox[0]),int(bbox[1]) - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255,0,0),2)
            cv2.rectangle(im,(bbox[0], bbox[1]),(bbox[2],bbox[3]),(100,255,100),3)        
    return im
 
def updateROIHistory(frame):
    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#RBG到HSV颜色空间转换
    #print hsv_roi
    mask = cv2.inRange(hsv_roi, np.array((0.,0.,32.)), np.array((180.,255.,255.)))
    roi_hist = cv2.calcHist([hsv_roi],[0],None,[180],[0,180 ])
### Load Video
cap = cv2.VideoCapture(INPUT_FILE)
 
width = cap.get(3)
height = cap.get(4)
fps = cap.get(5)
count = cap.get(7)
framspan = 1./fps
 
 
### Load Faster-R-CNN Model
cfg.TEST.HAS_RPN = True  # Use RPN for proposals
prototxt = os.path.join(cfg.MODELS_DIR, NETS['vgg16'][0],
                            'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                              NETS['vgg16'][1])
 
caffe.set_mode_gpu()
caffe.set_device(0)
cfg.GPU_ID = 0
net = caffe.Net(prototxt, caffemodel, caffe.TEST)
 
 
### Detect Object ! !
fourcc = cv2.VideoWriter_fourcc('M','P','4','2')
out = cv2.VideoWriter(OUTPUT_FILE, fourcc, fps, (int(width),int(height)), 1)

#存储帧序列和返回的值
rets=0
frames=[]
boundingBox=[] 
nextBoundingBox=[]
ret, firstFrame = cap.read()
if ret==True:
    print "ret is TURE"
    hsv_roi = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2HSV)#RBG到HSV颜色空间转换
    #print hsv_roi
    mask = cv2.inRange(hsv_roi, np.array((0.,0.,32.)), np.array((180.,255.,255.)))
    roi_hist = cv2.calcHist([hsv_roi],[0],None,[180],[0,180 ])
while(cap.isOpened()):
    for index in range(25):
        ret, frame = cap.read()
        if ret==True:
            frames.append(frame)
            rets+=1
        else:
            break
    if rets > 0:
        detectFrame = frames.pop()
        detectFrameResult = obj_detect(net, detectFrame)
        rets-=1
        while(rets > 0):
            rets-=1
            frame = frames.pop(0)
            frame=obj_track(frame)
            out.write(frame)
            cv2.imshow('Detection',frame)
            #追踪
        cv2.imshow('Detection',detectFrameResult)
        out.write(detectFrameResult) 
        updateROIHistory(detectFrame)  
    #threads = []
    #t1 = threading.Thread(target=obj_detect, args=(net,detectFrame))
    #frame = obj_detect(net, detectFrame)
    #if len(frames)>0:
    #追踪
 
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
