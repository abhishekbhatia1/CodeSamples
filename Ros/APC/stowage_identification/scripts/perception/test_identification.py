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

import pdb

import time

from utils/get_test_data import *
from utils/opencv_utils import *
from utils/picking_perception_utils import *
from utils/caffe_utils import *
from utils/visualization_utils import *

# Initialize network
# Network path information
reference_model = '/home/harp/apc_cnn/models/picking_id/deploy_superpix.prototxt'
reference_pretrained="/home/harp/apc_cnn/models/picking_id/_iter_50000.caffemodel"

# Set test parameters
TEST = 1
test_data_path = "/home/harp/apc_cnn/test_data/data_04_12/images/"

def main():
    # Only initialize network once
    # Also select GPU during runtime
    net = ID_net(reference_model, reference_pretrained, 0)
    if (TEST == 1):
        # Open text file for recording data
        text_file = open("results.txt", "w")
        # Load all image data
        data = image_data(test_data_path)
        for sample in range (len(data.image_list)):
            # Load image
            # Images loaded through openCV are BGR
            print "------------------------------------"
            print "Testing image number " + str(sample)
            image_file_path = data.image_list[sample]
            image = cv2.imread(image_file_path)
            possibleItems = data.item_list[sample]
            targetItem = possibleItems[0]
            print "Target item: " + getNames()[targetItem]

            identify_image(image, possibleItems, targetItem, net)

       
       
    #else()

if __name__ == "__main__":
    main()
