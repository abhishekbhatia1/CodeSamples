#!/usr/bin/env python

import sys
import rospy
from apc_msgs.srv import *
from apc_msgs.msg import *

import os.path

import pdb

import cv2
from cv_bridge import CvBridge, CvBridgeError

import matplotlib.pyplot as plt
import numpy as np

from sensor_msgs.msg import Image


if __name__ == "__main__":

    bridge = CvBridge()
    rospy.init_node('perception_test', anonymous=True)
    print "TEST initialized, waiting for server"
    rospy.wait_for_service('stowage_identification_srv')
    print "Server found, running test"
    stowage_identification = rospy.ServiceProxy('stowage_identification_srv', stowage_prediction)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        
        folder = '/home/harp/stowage_id_data/images/'
        for fn in os.listdir(folder):
            image_folder = folder
            print folder+fn
            image = cv2.imread(folder+fn)
            
            req = stowage_predictionRequest()
            # Save all data during testing
            possibleItems = range(38)
            # Input index should be 1-38
            possibleItems[:] = [x + 1 for x in possibleItems]

            req.possible_items = possibleItems
            req.img = bridge.cv2_to_imgmsg(image, "bgr8")
            res = stowage_identification(req)

            # Convert response back into numpy array
            predictions = list(res.prediction_results)
            predictions = np.asarray(predictions)
            predictions = np.reshape(predictions, (-1,38)) 
            pdb.set_trace()

            print predictions

            #print output_matrix 
            #out_fn = fn.replace(".jpg", "out")
            #saveName = '/home/harp/stowage_id_data/predictions/' + out_fn
            #self.imageCt += 1
            #np.savetxt(saveName, output_matrix, delimiter=',', fmt='%4f') 

        print "TEST COMPLETE"

        # TODO -- SAVE DATA

        rate.sleep()