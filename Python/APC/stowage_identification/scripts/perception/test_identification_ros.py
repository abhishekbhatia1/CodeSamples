#!/usr/bin/env python

import sys
import rospy
from apc_msgs.srv import *
from apc_msgs.msg import *
import pdb

import cv2
from cv_bridge import CvBridge, CvBridgeError

import matplotlib.pyplot as plt
import numpy

from sensor_msgs.msg import Image

from utils.get_test_data import *
from utils.picking_perception_utils import *

if __name__ == "__main__":

    bridge = CvBridge()
    rospy.init_node('perception_test', anonymous=True)
    print "TEST initialized, waiting for server"
    rospy.wait_for_service('picking_identification_srv')
    print "Server found, running test"
    picking_identification = rospy.ServiceProxy('picking_identification_srv', picking_id)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        test_data_path = "/home/harp/apc_cnn/test_data/data_04_12/images/"
        #test_data_path = "/home/harp/apc_cnn/test_data/temp/images/"
        data = image_data(test_data_path)
        for sample in range (len(data.image_list)):
            print "running test on sample " + str(sample)
            req = picking_idRequest()
            # Set input image
            image_file_path = data.image_list[sample]
            print "PATH: " + image_file_path
            image = cv2.imread(image_file_path)
            req.input_image = bridge.cv2_to_imgmsg(image, "bgr8")
            # Set bin target information
            possibleItems = data.item_list[sample]
            possibleItems = [x+1 for x in possibleItems]
            possibleItems.extend([0] * (10 - len(possibleItems)))
            targetItem = possibleItems[0]
            bin_in = bin()
            bin_in.name = "bin_A"
            bin_in.num_items = np.count_nonzero(possibleItems)
            bin_in.bin_contents = possibleItems
            bin_in.target_item = targetItem
            req.current_bin = bin_in
            print "Target item: " + getNames()[targetItem-1]
            print "Calling identification pipeline"
            res = picking_identification.call(req)
            print "Identification complete"
            
            output_image = res.output_image
            output_image = bridge.imgmsg_to_cv2(output_image, "bgr8")

            mask_file = data.mask_list[sample]
            ground_truth = cv2.imread(mask_file)

            score = scoreResult (output_image, ground_truth, targetItem)
            print score

        print "TEST COMPLETE"

        # TODO -- SAVE DATA

        rate.sleep()