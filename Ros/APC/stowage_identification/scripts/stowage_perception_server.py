#!/usr/bin/env python

import rospy
import random
from apc_msgs.srv import *
from std_srvs.srv import *
from apc_msgs.msg import *
import time
from cv_bridge import CvBridge, CvBridgeError
import cv2
import pdb
#from prediction_utilities import stowage_global_prediction, stowage_local_prediction
from GlobPred import pred
from GlobPred import bin_pred
import numpy as np
from json_exporter import json_exporter

class stowage_perception_server(object):
    def __init__(self):
        rospy.init_node('stowage_perception_server')
        self.srv = rospy.Service('get_target_stowage_bin', stowage_bins2target, self.service_cb)
        self.preprocess_stowage_image = rospy.ServiceProxy('preprocess_stowage_image', pc_2img)
        self.stowage_identification = rospy.ServiceProxy('stowage_identification_srv', stowage_prediction)
        self.bridge = CvBridge()
        self.count = 1
        self.rate = rospy.Rate(2) #hz
        self.imageCt = 0
        self.predictions = dict()
        self.item_list = []
        self.num_2_item_dict = rospy.get_param("/num_2_item_dict")
        self.img_to_bin = []
        self.old_prediction = []
        self.bin_list = []
        self.active_bins = [0, 1, 2]

        print "Stowage Perception Server Online, waiting for commands..."

    def service_cb(self, request):
        '''
            apc_msgs/bin[] bin_contents
            int8[] tote_contents
            ---
            int8 target_bin
        '''
        response = stowage_bins2targetResponse()

        print "Service Call recieved"
        ''' Call mask_world '''
        #eventuall 
        #self.item_list = 
        #for now
        #self.item_list = [6, 4, 11, 13, 14, 15, 21,  23, 29, 32, 33, 30]
        self.item_list = request.tote_contents

        print "Possible items :::::::"
        for item in self.item_list:
            print self.num_2_item_dict[str(item)]


        ''' 1) Perform Pointcloud Segmentation  ******************'''

        req = pc_2imgRequest()   
        res = self.preprocess_stowage_image(req)
        #Result        
        initial_image = res.img1
        identification_image = res.img2
        print "Masked image"



        ''' 2) Perform CNN to get Image Prediction  *****************'''
        
        req = stowage_predictionRequest()       
        req.img = identification_image
        req.possible_items = self.item_list
        res = self.stowage_identification (req)

        # Convert response back into numpy array
        CNN_prediction = list(res.prediction_results)
        CNN_prediction = np.asarray(CNN_prediction)
        CNN_prediction = np.reshape(CNN_prediction, (38,-1)) 
        self.predictions[self.imageCt] = CNN_prediction

	print "CNN Prediction is: "
	print CNN_prediction

        



        ''' 3) perform prediction on all available images ******************* '''
        prediction, crap1, crap2, confidence = pred(self.count, self.item_list, self.predictions)
        self.bin_list = bin_pred(prediction, self.old_prediction, self.active_bins, self.bin_list)
        self.old_prediction = prediction
        ''' prediction shape = (images,1)
            actual_item list - unneeded in online testing
            total_prediction - unneeded in online testing
            confidence - 12 x 12 probability
        '''

        print "\nprediction is: " ,prediction
        #printstring = []
        #for i in range(0,len(prediction)):
        #    printstring.append(self.num_2_item_dict[int(prediction[i])])
        #print printstring
   
        print ' confidence is: ' 
	np.set_printoptions(precision=0)
	for r in range(0,12):
		string = []
		for c in range(0,12):
			string.append(round(confidence[r][c]*100.0))
		print string


	print "\nbin_list is: ", self.bin_list







        ''' 4) assign item to target shelf bin ****************** '''
        
        #TODO implement logic to understand if the item is confusable
        confusable = 0;
        prediction_is_small = 1;
        target_bin = 0;
        if(confusable):
            # place on target bin of other confusable item
            pass
        elif(not prediction_is_small):
            # item is large
            pass
        else:
            #target_bin = self.imageCt/3 + 2
            target_bin = self.bin_list[len(self.bin_list) - 1]
        self.img_to_bin.append(target_bin)
        print "Target bin:" , target_bin
        response.target_bin = target_bin


        ''' 5) update the shelf belief state and send out message for JSON printing '''
        bin_names = ["bin_A","bin_B","bin_C","bin_D","bin_E","bin_F","bin_G", "bin_H","bin_I", "bin_J", "bin_K", "bin_L"]
        from apc_msgs.msg import bin
        shelf_state = []
        for i in range(0,12):
            shelf_state.append(bin())
	
        for i in range(0,12):
            tup = request.bin_contents[i].bin_contents
            ll = []
            for t in tup:
                ll.append(t)
            shelf_state[i].bin_contents = ll
            shelf_state[i].name = bin_names[i]

                
        for i, item in enumerate(prediction):
            bin_num = self.img_to_bin[i]
            shelf_state[i].bin_contents.append(item);

        for bin in shelf_state:
            print bin.bin_contents  
        #TODO Send to JSON exporter on master cpu
        json_exporter(shelf_state, 'FINAL_SHELF_CONTENTS.json', self.num_2_item_dict)

        ''' Save Results ********************'''
        # result_cloud = []
        rawName = '/home/harp/Desktop/stowage_roboauto_images/raw-' + str(self.imageCt) + '.jpg'
        maskName = '/home/harp/Desktop/stowage_roboauto_images/segmented-' + str(self.imageCt) + '.jpg'

        cv_image_raw = self.bridge.imgmsg_to_cv2(initial_image, "bgr8")
        cv_image_mask = self.bridge.imgmsg_to_cv2(identification_image, "bgr8")

        cv2.imwrite(rawName, cv_image_raw)
        cv2.imwrite(maskName, cv_image_mask)


        ''' update counters and return **************** '''
        self.imageCt +=1
        self.count += 1

        return response

    def run(self):

        rospy.wait_for_service('stowage_perception_server')
        rospy.wait_for_service('stowage_identification_srv')

        while not rospy.is_shutdown():
            self.rate.sleep()
    


if __name__ == "__main__":
    server = stowage_perception_server()
    server.run()
