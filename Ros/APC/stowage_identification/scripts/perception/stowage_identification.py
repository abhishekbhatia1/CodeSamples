#!/usr/bin/env python

import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import os.path
import json
import scipy
import argparse
import math
import pylab
import cv2
import IPython
import pdb

import rospy
import rospkg
from apc_msgs.srv import *
from std_srvs.srv import *
from apc_msgs.msg import *

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv_bridge

from utils.get_test_data import *
from utils.opencv_utils import *
from utils.picking_perception_utils import *
from utils.caffe_utils import *
from utils.visualization_utils import *

class stowage_perception:
    def __init__(self, model, weights):
        self.net = ID_net(model, weights, 0)
        self.output_img = []
        self.labeled_img = []
        self.do_pub = 0
        self.bridge = CvBridge()
        self.imageCt = 0
        return

    def get_image(self, data):
        image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        return image

    def scene_prediction(self,req):
        # Note image is in BGR format
        print "Prediction called"

        image = self.get_image(req.img)

        possibleItems = list(req.possible_items)
        # Item indexes based on 
        #possibleItems = [1,  2,  3,
        #                  4,  5,  6,
        #                  7,  8,  9,
        #                  10, 15, 21]
        # OFF BY ONE!!! Prediction expects 0 to n-1 labels
        possibleItems[:] = [x - 1 for x in possibleItems]


        #output_mask = identify_image(image, possibleItems, targetItem, self.net)
        output_matrix = predict_stowage(image, possibleItems, self.net)

        #print output_matrix
        output_matrix = np.asarray(output_matrix)
        output_matrix = output_matrix.transpose()
        output_vector = output_matrix.flatten()
        output_vector.tolist()

        print output_vector
        
        res = stowage_predictionResponse()
        res.prediction_results = output_vector

        #res.output_image = self.bridge.cv2_to_imgmsg(image, "bgr8")

        #self.output_img = output_mask
        #self.labeled_img = best_image
        #self.do_pub = 1
        print "Made prediction, Returning"
        return res


if __name__ == "__main__":

    # Init Node
    rospy.init_node('stowage_identification')
    # Initialize network
    # Todo update package paths
    rospack = rospkg.RosPack()
    model = rospack.get_path('stowage_identification') + "/models/caffe/id_cnn/deploy_superpix.prototxt"
    weights = rospack.get_path('stowage_identification') + "/models/caffe/id_cnn/id_20160412.caffemodel"     
    object_recognition = stowage_perception(model, weights)

    print "Initialized"
    # Launch classification service
    # 
    service = rospy.Service('stowage_identification_srv', stowage_prediction, object_recognition.scene_prediction)
    # Results publisher
    # scene_publisher = rospy.Publisher("/identification_results",  Image, queue_size = 1)
    # result_publisher = rospy.Publisher("/item_of_interest", Image, queue_size = 1)
    # Spin ROS
    print 
    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        #print "HERE"
        #if (object_recognition.do_pub):
        #    labeled_output = net.bridge.cv2_to_imgmsg(net.labeled_img, "bgr8")
        #    id_image = object_recognition.bridge.cv2_to_imgmsg(object_recognition.output_img, "bgr8")
        #    scene_publisher.publish(labeled_output)
        #    result_publisher.publish(id_image)
        #    object_recognition.do_pub = 0
        rate.sleep()    
