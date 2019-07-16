from config import cfg
from test import im_detect
from nms_wrapper import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
plt.switch_backend('SVG')
import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2, operator
import argparse
import shutil
from operator import itemgetter
CLASSES = ('__background__',
            'star')

NETS = {'vgg16': ('VGG16',
                  'VGG16_faster_rcnn_final.caffemodel'),
        'zf': ('ZF',
                  'ZF_faster_rcnn_final.caffemodel')}
path='./result'
if os.path.exists(path):
    shutil.rmtree(path)
os.mkdir(path)
txt=os.path.join(path,'result_top3.txt')
def vis_detections(im, class_name, dets, image_name, thresh=0.1):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return
    im = im[:, :, (2, 1, 0)]
    height, width, channels = im.shape
    fig, ax = plt.subplots()
     
    # fig, ax = plt.figure(image_name)
    ax.imshow(im, aspect='equal')
    LL=[]
    for i in inds:
    	bbox = dets[i,:4]
    	score=dets[i,-1]
    	MM=[bbox[0],bbox[1],bbox[2],bbox[3],score]
    	LL.append(MM)
    N=sorted(LL, key=itemgetter(4), reverse=True)
    count=0
    for bbox in N:
      if(count<3):

          if(class_name=='__background__'):
              fw=open(txt,'a',newline='')
              # csv_write=csv.writer(fw,dialect='excel')
              # stu=[str(image_name),class_name,str(int(bbox[0])),str(int(bbox[1])),str(int(bbox[2])),str(int(bbox[3])),str(int(bbox[3])),str(score)]
              # csv_write.writerow(stu)
              fw.write(str(image_name)+' '+class_name+' '+str(int(bbox[0]))+' '+str(int(bbox[1]))+' '+str(int(bbox[2]))+' '+str(int(bbox[3]))+' '+str(bbox[4])+'\n')
              fw.close()
          elif(class_name=='star'):
              fw=open(txt,'a')
              # csv_write=csv.writer(fw,dialect='excel')
              # stu=[str(image_name),class_name,str(int(bbox[0])),str(int(bbox[1])),str(int(bbox[2])),str(int(bbox[3])),str(int(bbox[3])),str(score)]
              # csv_write.writerow(stu)
              fw.write(str(image_name)+' '+class_name+' '+str(int(bbox[0]))+' '+str(int(bbox[1]))+' '+str(int(bbox[2]))+' '+str(int(bbox[3]))+' '+str(bbox[4])+'\n')
              fw.close()
          ax.add_patch(
              plt.Rectangle((bbox[0], bbox[1]),
                            bbox[2] - bbox[0],
                            bbox[3] - bbox[1], fill=False,
                            edgecolor='red', linewidth=0.5)
              )
          ax.text(bbox[0], bbox[1] - 2,
                  '{:s} {:.3f}'.format(class_name, bbox[4]),
                  bbox=dict(boxstyle="rarrow",pad=0.2,facecolor='blue', alpha=0.5),
                  fontsize=2, color='white')
          count=count+1
    plt.axis('off')
    fig.set_size_inches(width/100.0/3.0, height/100.0/3.0) 
    plt.gca().xaxis.set_major_locator(plt.NullLocator()) 
    plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
    plt.margins(0,0)
    plt.draw()
    # plt.savefig("/home/shelly/py-faster/data/trial_top3/"+image_name,dpi=300)

    # plt.savefig("/home/shelly/py-faster/data/trial_top3/"+image_name)


def demo(net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    # im_file = os.path.join('/home/shelly/superstar/star/SuperNova/static/upload',image_name)
	# change filepath
    im_file = os.path.join('/home/shelly/flask/star/star/SuperNova/static/upload',image_name)
    im = cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.1
    NMS_THRESH = 0.3
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        vis_detections(im, cls, dets, image_name, thresh=CONF_THRESH)

# def parse_args():
#     """Parse input arguments."""
#     parser = argparse.ArgumentParser(description='Faster R-CNN demo')
#     parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
#                         default=0, type=int)
#     parser.add_argument('--cpu', dest='cpu_mode',
#                         help='Use CPU mode (overrides --gpu)',
#                         action='store_true')
#     parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
#                         choices=NETS.keys(), default='vgg16')
#     parser.add_argument('--model', dest='model_dir',
#                         help='model save dir',
#                         default='static/model', type=str)

    # args = parser.parse_args()

    # return args

def test(a):
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    # args = parse_args()

    prototxt = 'static/model/faster_rcnn_test.pt'
    caffemodel = 'static/model/VGG16_faster_rcnn_final.caffemodel'

    if not os.path.isfile(caffemodel):
        raise IOError(('{:s} not found.\nDid you run ./data/script/'
                       'fetch_faster_rcnn_models.sh?').format(caffemodel))

    caffe.set_mode_gpu()
    caffe.set_device(0)
    cfg.GPU_ID = 0
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)

    print '\n\nLoaded network {:s}'.format(caffemodel)

    # Warmup on a dummy image
    im = 128 * np.ones((300, 500, 3), dtype=np.uint8)
    for i in xrange(2):
        _, _= im_detect(net, im)

    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Demo for data/demo/{}'.format(a)
    demo(net, a)

    # plt.savefig("/home/shelly/superstar/star/SuperNova/index/static/test3.jpg",dpi=300)
	# change filepath
    plt.savefig("/home/shelly/flask/star/star/SuperNova/index/static/test3.jpg",dpi=300)