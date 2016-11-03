#!/usr/bin/env python

import rospy
from apc_msgs.srv import *
from std_srvs.srv import *
from apc_msgs.msg import *
import numpy as np
import json


class stowage_json_exporter(object):
    def __init__(self):
        rospy.init_node('stowage_json_exporter')
        self.srv = rospy.Service('write_stowage_json', stowage_bins2target, self.service_cb)


        print "json exporter Server Online, waiting for commands..."

    def service_cb(self, request):
        '''
            apc_msgs/bin[] bin_contents
            int8[] tote_contents
            ---
            int8 target_bin


            bin.msg
                string name
                uint64 num_items
                uint64[] bin_contents
                uint64 target_item
        '''
        

        response = stowage_bins2targetResponse()
        return response

    def run(self):

        rospy.wait_for_service('stowage_perception_server')
        rospy.wait_for_service('stowage_identification_srv')

        while not rospy.is_shutdown():
            self.rate.sleep()
    


if __name__ == "__main__":
    server = stowage_perception_server()
    server.run()