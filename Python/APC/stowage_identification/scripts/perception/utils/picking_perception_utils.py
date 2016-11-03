#!/usr/bin/env python

import cv2

import numpy as np

import warnings
import pdb

from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from sklearn import cluster

import pydensecrf.densecrf as dcrf

import time

from pylab import *
from scipy.ndimage import measurements

from get_test_data import *
from opencv_utils import *
from caffe_utils import *
from visualization_utils import *

# Graph data structure
class Segment():
    def __init__(self, cx, cy, neighbors, image, raw, norm):
        self.cx = cx
        self.cy = cy
        self.neighbors = neighbors
        self.image = image
        self.raw_prediction = raw
        self.norm_prediction = norm

# Returns the full image and the 256x256 image of a given superpixel
def getSuperpixel(image,
                  segments, 
                  segVal,
                  output_mask,
                  masked_image,
                  count):
    segmask = np.zeros(image.shape[:2], dtype = "uint8")
    segmask[segments == segVal] = count
    output_mask = output_mask|segmask 
    # Save masked image, for later network training
    # Find COM, crop to 256x256 region
    M = cv2.moments(masked_image[:,:,0])
    s = 256
    cx, cy = findCOM(masked_image,s)
    segment_crop = masked_image[cy-s/2:cy+s/2,cx-s/2:cx+s/2,:]
    return segment_crop,output_mask        

def do_slic(num_segments, comp, image):
    # Supress warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        segments = slic(img_as_float(image),
                        n_segments = num_segments, 
                        sigma = 0,
                        compactness = comp,
                        convert2lab=True)
    return segments

# Finds neighboring superpixels for a given superpixel
def getNeighbors(image, output_mask, superpic_val):
    # Generate mask around segment i
    segment_mask = np.zeros(image.shape[:2], dtype = "uint8")
    segment_mask[output_mask == superpic_val] = 10 

    # DST is a mask, with a 5X5 kernel applied, so segment should slightly grow
    kernel = np.ones((5,5),np.float32)
    dst = cv2.filter2D(segment_mask,-1,kernel)
    dst = np.minimum(np.ones(image.shape[:2], dtype = "uint8"), dst)
    dst = dst * 255

    # Apply mask to segment mask
    superpix_mask = cv2.bitwise_and(output_mask, output_mask, mask = dst)
    # get neighbors
    neighbors = np.unique(superpix_mask)
    neighbors = np.trim_zeros(neighbors)
    neighbors = np.setdiff1d(neighbors, np.array([superpic_val]))
    neighbors = np.subtract(neighbors, 1)

    M = cv2.moments(segment_mask)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    return neighbors,cx,cy

# Generates a graph of all neighboring superpixels
def generateGraph(image, output_mask, imageArray, rawPredictionArray, normPredictionArray):
    num_segments = np.amax(output_mask)
    graph = []
    # Create graph
    for i in range (num_segments):
        superpic_val = i+1

        neighbors,cx,cy = getNeighbors(image, 
                                 output_mask, 
                                 superpic_val)
        # Add graph to segment
        seg = Segment(cx, cy, 
                      neighbors,
                      imageArray[i],
                      rawPredictionArray[i],
                      normPredictionArray[i])
        graph.append(seg)

    return graph

# Overlay graph on top of image
def drawGraph(image, graph):
    graph_image = np.copy(image)
    for seg in graph:
        for n in seg.neighbors:
            cx1 = seg.cx
            cy1 = seg.cy
            index = n
            seg2 = graph[index]
            cx2 = seg2.cx
            cy2 = seg2.cy
            cv2.line(graph_image, (cx1,cy1), (cx2,cy2),(255, 0, 0),2)
    return graph_image

def singleItemID(image, graph, targetItem):

    best_score = 0 
    best_node = []
    ct = 0
    for node in graph:
        score = node.raw_prediction[targetItem]
        #print node.norm_prediction
        #print node.neighbors
        for neighbor_index in node.neighbors:
            neighbor = graph[neighbor_index]
            neighbor_score = neighbor.raw_prediction[targetItem]
            score += .5 * neighbor_score
        ct = ct + 1
        if (score > best_score):
            best_node = node
            best_score = score

    output_mask = np.zeros(image.shape, dtype = "uint8")
    node_image = best_node.image
    output_mask = output_mask|node_image
    for neighbor_index in best_node.neighbors:
        neighbor = graph[neighbor_index]
        node_image = neighbor.image
        output_mask = output_mask|node_image

    return output_mask


def computeDenseCRF(image, output_mask, graph, numItems):
    # Class for each of 38 items, plus none
    numClasses = numItems + 1

    h,w,c = image.shape

    d = dcrf.DenseCRF2D(w, h, numClasses, dtype="float32")

    U = np.zeros([numClasses,w,h])
    prob_v = np.zeros(numClasses)+.000001
    prob_v[-1] = 1
    U[0:-1,:,:]=-np.log(.000001)
    U[-1,:,:]=-np.log(1)

    height, width = output_mask.shape
    #TODO cache log calculations
    #Verify improvement 
    t1 = time.time()
    for i in range (height):
        for j in range (width):
            val = output_mask[i,j]
            if (val == 0):
                pass
            else:
                prob_v = np.zeros(numClasses)+.000001
                seg = graph[val-1]
                prob_v[0:-1]= prob_v[0:-1] + seg.norm_prediction 
                U[:,j,i]=-np.log(prob_v)
    t2 = time.time()
    print "Made Array in %3f seconds" % (t2-t1)

    U = U.astype("float32")

    U = U.reshape(numClasses,-1)
    d.setUnaryEnergy(U)
    # This adds the color-independent term, features are the locations only.
    d.addPairwiseGaussian(sxy=(3,3), compat=3, kernel=dcrf.DIAG_KERNEL, normalization=dcrf.NORMALIZE_SYMMETRIC)
    # This adds the color-dependent term, i.e. features are (x,y,r,g,b).
    d.addPairwiseBilateral(sxy=(80, 80), srgb=(13, 13, 13), rgbim=image,
                           compat=10,
                           kernel=dcrf.DIAG_KERNEL,
                           normalization=dcrf.NORMALIZE_SYMMETRIC)
    Q = d.inference(3)
    out_map = np.argmax(Q, axis=0).reshape((width,height))

    res = out_map.astype('float32') * 255 / out_map.max()
    res = np.swapaxes(res,0,1)
    res = res.astype('uint8')

    return out_map

def getTargetOutput(image, targetItem, out_map):
    # Find item labeled output from CRF
    item_label = np.zeros(out_map.shape,dtype="uint8")
    item_index = (out_map == targetItem)
    item_label[item_index]=1
    # Label segments and calculate max area
    lw, num = measurements.label(np.asarray(item_label))
    area = measurements.sum(item_label, lw, index=arange(lw.max() + 1))
    best_val = np.argmax(area)
    # Mask image, create single segment
    image_mask = np.zeros(out_map.shape,dtype="uint8")
    best_index = (lw == best_val)
    image_mask[best_index] = 1
    image_mask = np.swapaxes(image_mask,0,1)
    #image_mask = np.swapaxes(image_mask,0,1)
    final_mask = np.zeros(image.shape, dtype="uint8")
    # Hack, dont know why repmat wont work...
    final_mask[:,:,0] = image_mask
    final_mask[:,:,1] = image_mask
    final_mask[:,:,2] = image_mask
    final_mask_index = (final_mask == 0)
    image_out = np.copy(image)
    image_out[final_mask_index] = 0

    return image_out

def identify_image(image, possibleItems, targetItem, net):
    # Set slic parameters, these should be equal during train and test
    num_segments = 1000
    comp = 30

    # Misc. runtime params
    show_slic = 0
    save_superpixels = 0
    show_graph = 0
    show_result = 0

    print "Running SLIC"
    t0 = time.time()
    segments = do_slic(num_segments, comp, image)
    if (show_slic == 1):
        visualize_slic(image, segments)
    # Run prediction on each superpixel
    t1 = time.time()
    print "Ran SLIC in %3f seconds" % (t1-t0)
    
    print "Classifying Superpixels"
    t0 = time.time()
    (output_mask, 
    imageArray, 
    segmentArray,
    rawPredictionArray, 
    normPredictionArray) = net.classifySuperpixels(image, 
                                                  segments, 
                                                  possibleItems)
    t1 = time.time()
    print "Ran classification in %3f seconds" % (t1-t0)

    if (save_superpixels == 1):
        do_save_superpixels(segmentArray, )
        #save_name = image_file.replace("images", "results/pix")
    #   save_name = save_name.replace(".jpg", "_"+str(i)+".jpg")
    #   cv2.imwrite(save_name,segment_crop)

    # Generate a graph of connecting superpixels
    print "Generating Graph"
    t0 = time.time()
    graph = generateGraph(image, output_mask, imageArray, rawPredictionArray, normPredictionArray)
    t1 = time.time()
    print "Generated graph in %3f seconds" % (t1-t0)

    if (show_graph == 1):
        graph_image = drawGraph(image, graph)
        plt.axis("off")
        plt.imshow(cv2.cvtColor(graph_image, cv2.COLOR_BGR2RGB))
        plt.show()

    if (len(possibleItems) == 0):
        print "Running CRF"
        t0 = time.time()
        numItems = len(getNames())
        out_map = computeDenseCRF(image, output_mask, graph, numItems);
        t1 = time.time()
        print "Ran CRF in %3f seconds" % (t1-t0)
        #res = out_map.astype('float32') * 255 / out_map.max()
        #plt.imshow(res)
        #plt.show()

        print "Identifying Target Item " + getNames()[targetItem]
        t0 = time.time()
        identification_result = getTargetOutput(image, targetItem, out_map)
        t1 = time.time()
        print "Identified item in %3f seconds" % (t1-t0)
        if (show_result == 1):
            plt.axis("off")
            plt.imshow(cv2.cvtColor(identification_result, cv2.COLOR_BGR2RGB))
            plt.show()

    else:
        print "IDENTIFYING BEST SEGMENT"
        t0 = time.time()
        numItems = len(getNames())
        identification_result = singleItemID(image, graph, targetItem)
        t1 = time.time()
        print "Identified single item in %3f seconds" % (t1-t0)        

    return identification_result


def predict_stowage(image, possibleItems, net):
    # Set slic parameters, these should be equal during train and test
    num_segments = 1000
    comp = 30
    
    # Misc. runtime params
    show_slic = 0
    #save_superpixels = 0
    #show_graph = 0
    #show_result = 0

    print "Running SLIC"
    t0 = time.time()
    segments = do_slic(num_segments, comp, image)
    if (show_slic == 1):
        visualize_slic(image, segments)
    # Run prediction on each superpixel
    t1 = time.time()
    print "Ran SLIC in %3f seconds" % (t1-t0)

    print "Classifying Superpixels"
    t0 = time.time()
    #minSize = 20
    (output_mask, 
    imageArray, 
    segmentArray,
    rawPredictionArray, 
    normPredictionArray) = net.classifySuperpixels(image, 
                                                  segments, 
                                                  possibleItems)
    t1 = time.time()
    print "Ran classification in %3f seconds" % (t1-t0)  

    print rawPredictionArray 

    return rawPredictionArray

def scoreResult (output_image, ground_truth, targetItem):
    
    image_mask = output_image[:,:,0]
    item_index = (image_mask != 0)
    image_mask[item_index] = 1 

    gt = zeros(ground_truth.shape, dtype="uint8")
    item_index = (ground_truth == targetItem)
    gt[item_index] = 1
    gt = gt[:,:,0]
    #pdb.set_trace()
    # Calculate innersection over union
    overlap = np.count_nonzero(image_mask&gt)
    total = np.count_nonzero(image_mask|gt)
    IOU = overlap*1.0/total
    return IOU    