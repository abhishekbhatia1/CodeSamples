#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
#from sklearn.preprocessing import normalize

# TODO clean up imports
import os.path
import json
import scipy
import argparse
import math
import pylab
from random import randint
# New lab machine
#caffe_root = '/home/harp/src/caffe/' 
# Ricks laptop
caffe_root = '/home/rshanor/src/caffe/' 
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe

import pdb

import rospy
import rospkg

import cv2
from cv_bridge import CvBridge, CvBridgeError

from apc_msgs.srv import *
from std_srvs.srv import *
from apc_msgs.msg import *
from sensor_msgs.msg import Image

# names = ["LOL", #0
# "glucose", #1
# "coffee", #2
# "elmers", #3
# "shirt", #4
# "eggs", #5
# "glue", #6
# "brush", #7
# "hooks", #8
# "cup", #9
# "tape"] #10

# names = ["brush", #0
# "elmers", #1
# "index", #2
# "LOL", #3
# "eggs"] #10

class ID_net:
    def __init__(self, model, pretrained):
        self.net = caffe.Classifier(
          reference_model,
          reference_pretrained)
        self.transformer = self.get_transformer()
        self.bridge = CvBridge()
        # Load an image for testing... 
        self.image = []
        self.test = 1
        self.debug = 1

        self.names=names = ["LOL", #0
                            "glucose", #1
                            "coffee", #2
                            "elmers", #3
                            "shirt", #4
                            "eggs", #5
                            "glue", #6
                            "brush", #7
                            "hooks", #8
                            "cup", #9
                            "tape"] #10

    def predict(self, req):
        itemNumber = 0
        #if (self.test == 1):
        #    name, itemNumber = self.get_random_image()
        #    self.image = caffe.io.load_image(name)

        self.net.blobs['data'].reshape(1,3,227,227)
        self.net.blobs['data'].data[...] = self.transformer.preprocess('data', self.image)
        out = self.net.forward()
        predictions = out['prob']
        rand_i = str((randint(0,100000)))
        print rand_i
        for i in range (3):
            predicted_class_index = predictions.argmax()
            print "Prediction: " + self.names[predicted_class_index] + \
                    "  Prob: " + str(predictions[0,predicted_class_index])
            predictions[0,predicted_class_index]=0
        print "------------------------"
        # if (self.test == 1):
        #     print "Prediction: " + self.names[predicted_class_index] + \
        #       "   Correct Answer: " + self.names[itemNumber]
        # else: print "Prediction: " + self.names[predicted_class_index] + \
        #             "  Prob: " + str(predictions[0,predicted_class_index])
        if (self.debug == 1):
            # NOTE, for some reason, this only works 
            filename = "/home/rshanor/id_data/" + rand_i + ".jpg"
            cv2.imwrite(filename, cv2.cvtColor(self.image*255, cv2.COLOR_RGB2BGR))
            #cv2.startWindowThread()
            #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            #cv2.imshow('image',cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            #cv2.waitKey(1)
            #plt.imshow(self.image)
            #plt.show()
            pass
        return

    def get_transformer(self):
        transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        transformer.set_transpose('data', (2,0,1))
        # TODO Test both ways, if we load image as BRG this should be unnecessary
        # Should confirm this though...
        transformer.set_channel_swap('data', (2,1,0)) 
        transformer.set_raw_scale('data', 255.0)       
        return transformer

    def get_random_image(self):
        # NOTE: TEST SET SOLUTIONS FOR 5 ITEM SET
        images = ['0000_color.jpg',
                  '0001_color.jpg',
                  '0002_color.jpg',
                  '0003_color.jpg',
                  '0004_color.jpg',
                  '0005_color.jpg',
                  '0006_color.jpg',
                  '0007_color.jpg',
                  '0008_color.jpg',
                  '0009_color.jpg',
                  '0010_color.jpg',
                  '0011_color.jpg',
                  '0012_color.jpg',
                  '0013_color.jpg',
                  '0014_color.jpg']
        path = '/home/rshanor/id_cnn/test_images/'
        img_ct = len(images)
        index = (randint(0,img_ct-1))
        answer = [0,0,0,3,3,3,4,4,4,1,1,1,2,2,2]
        return path + images[index], answer[index]

    def get_image(self, data):
        #if (self.test == 0):
            #self.image = caffe.io.load_image("/home/harp/apc/collection/downsample/temp/images/0065_color.jpg")
            #self.test = 1
        # Convert from Kinect MSG to CNN Input
        # TODO ensure this is the right input format
        image = self.bridge.imgmsg_to_cv2(data, "rgb8")
        image = np.array(image,dtype=np.float32)/255
        self.image = image
        self.test = 0

if __name__ == "__main__":

    # Init Node
    rospy.init_node('ID_CNN')
    # Set Caffe to use GPU
    caffe.set_mode_gpu()
    caffe.set_device(0) # MODIFY FOR 2 GPU MACHINE
    # Path to Caffe model
    #reference_model = '/home/harp/SegNet-Tutorial/id_cnn/deploy_new2.prototxt'
    #reference_pretrained = '/home/harp/SegNet-Tutorial/id_cnn/models/_iter_10000.caffemodel'
    rospack = rospkg.RosPack()
    reference_model = rospack.get_path('apc') + "/models/caffe/id_cnn/eleven_item_deploy.prototxt"
    reference_pretrained = rospack.get_path('apc') + "/models/caffe/id_cnn/eleven_item.caffemodel"
    # Load network 
    net = ID_net(reference_model, reference_pretrained)
    # Launch classification service
    service = rospy.Service('id_cnn', Empty, net.predict)
    # Launch image subscriber 
    image_sub = rospy.Subscriber("/stowage_segmented_image", Image, net.get_image)
    # Launch 
    # roi_sub = rospy.Subscriber("/image_roi", roi, net.get_roi)
    # Image publisher
    #output_pub = rospy.Publisher("/cnn_mask", Image, queue_size = 1)
    # Spin ROS
    rate = rospy.Rate(3)
    while not rospy.is_shutdown():
        #if (net.doPub):
        #    output_pub.publish(net.imageOut)
        rate.sleep()
