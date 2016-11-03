#!/usr/bin/env python
import roslib
import rospy
import sys
from sensor_msgs.msg import Image
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError

topicName = "camera/image_raw"
pubName = "flipped"

class flip:
	def __init__(self):
		
		global pubName
		global topicName
		self.bridge = CvBridge()
		self.sub = 	rospy.Subscriber("apb_camera/image_raw",Image, self.callback)		
		self.pub =  rospy.Publisher("apb_flipped", Image)

	def callback(self,data):
		cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		(rows,cols,channels) = cv_image.shape
	
		flipped_image = cv_image.copy()
		for i in range(0,rows):
			from_row = cv_image[rows-i-1, :]
			flipped_image[i ,:] = from_row		
		
		try:
			self.pub.publish(self.bridge.cv2_to_imgmsg(flipped_image, "bgr8") )
		except CvBridgeError, e:
			print e
			
def main(args):
	global topicName
	topicName = args[1]
	pubName = args[2]
	print("topic name is " + topicName)
	print("pub name is " + pubName)
	rospy.init_node('flip', anonymous = True)
	flipper_makes_a_splash = flip()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	main(sys.argv)
