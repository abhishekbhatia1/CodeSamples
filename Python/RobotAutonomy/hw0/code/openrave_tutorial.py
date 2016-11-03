#!/usr/bin/env python

PACKAGE_NAME = 'hw0'

# Standard Python Imports
import os
import copy
import time
import numpy as np
import scipy

# OpenRAVE
import openravepy
from openravepy import *
#openravepy.RaveInitialize(True, openravepy.DebugLevel.Debug)


curr_path = os.getcwd()
relative_ordata = '/models'
ordata_path_thispack = curr_path + relative_ordata

#this sets up the OPENRAVE_DATA environment variable to include the files we're using
openrave_data_path = os.getenv('OPENRAVE_DATA', '')
openrave_data_paths = openrave_data_path.split(':')
if ordata_path_thispack not in openrave_data_paths:
  if openrave_data_path == '':
    os.putenv('OPENRAVE_DATA', ordata_path_thispack)
  else:
    os.putenv('OPENRAVE_DATA', '%s:%s'%(ordata_path_thispack, openrave_data_path))


class RoboHandler:
  def __init__(self):
    self.env = openravepy.Environment()
    self.env.SetViewer('qtcoin')
    self.env.GetViewer().SetName('Tutorial Viewer')
    self.env.Load('models/%s.env.xml' %PACKAGE_NAME)
    # time.sleep(3) # wait for viewer to initialize. May be helpful to uncomment
    self.robot = self.env.GetRobots()[0]
    

  #remove all the time.sleep(0) statements! Those are just there so the code can run before you fill in the functions

  # move in a straight line, depending on which direction the robot is facing
  def move_straight(self, dist):
    #TODO Fill in, remove sleep
    time.sleep(0)
    tr = np.array([ [1.0, 0, 0, dist], [0, 1.0, 0, 0], [0, 0, 1.0, 0], [0, 0, 0, 1.0] ])
    with self.env:
      for self.robot in self.env.GetRobots():
        self.robot.SetTransform(np.dot(self.robot.GetTransform(),tr))


  # rotate the robot about the z-axis by the specified angle (in radians)
  def rotate_by(self, ang):
    #TODO Fill in, remove sleep
    tz = matrixFromAxisAngle([0,0,ang])
    with self.env:
      for self.robot in self.env.GetRobots():
        self.robot.SetTransform(np.dot(self.robot.GetTransform(),tz))

  # go to each of the square corners, point towards the center, and snap a photo!
  def go_around_square(self):
    #TODO Fill in
    robo.move_straight(1)
    time.sleep(2)
    robo.rotate_by(np.pi/2)
    time.sleep(2)
    robo.move_straight(1)
    time.sleep(2)
    for i in range(4):
        robo.rotate_by(np.pi*3/4)
        time.sleep(2)
        robo.rotate_by(-np.pi/4)
        time.sleep(2)
        robo.move_straight(2)
        time.sleep(2)
    robo.rotate_by(np.pi*3/4)
    time.sleep(2)
    # set the robot back to the initialize position after
    with self.env:
      self.robot.SetTransform(np.identity(4)); 

  # a function to help figure out which DOF indices correspond to which part of HERB
  def figure_out_DOFS(self):
    #TODO Fill in, remove sleep
    time.sleep(0)
    with self.env:
      for self.robot in self.env.GetRobots():
        dof=self.robot.GetDOF()
        for i in range(dof):
          jfdi=self.robot.GetJointFromDOFIndex(i)
          print(jfdi)
  
  # put herb in self collision
  def put_in_self_collision(self):
    #TODO Fill in, remove sleep
    time.sleep(0)
    with self.env:
      for self.robot in self.env.GetRobots():
        #self.robot.SetDOFValues([-.1,np.pi,.1,np.pi],[2,3,13,14])
        self.robot.SetDOFValues([np.pi,np.pi,2*np.pi,2*np.pi],[3,14,1,12])
        
  # saves an image from above, pointed straight down
  def save_viewer_image_topdown(self, imagename):
    TopDownTrans = np.array([ [0, -1.0, 0, 0], [-1.0, 0, 0, 0], [0, 0, -1.0, 5.0], [0, 0, 0, 1.0] ])
    #seems to work without this line...but its in the tutorial, so I'll keep it here in case
    self.env.GetViewer().SendCommand('SetFiguresInCamera 1') # also shows the figures in the image
    I = self.env.GetViewer().GetCameraImage(640,480,  TopDownTrans,[640,640,320,240])
    scipy.misc.imsave(imagename + '.jpg',I)
      

if __name__ == '__main__':
  robo = RoboHandler()

  # Uncomment the following and comment the `while` block to make the script initialize the RoboHandler
  #  and dr op you into an IPython shell after starting IPython and doing execfile('openrave_tutorial.py').
  t = np.array([ [0, -1.0, 0, 0], [-1.0, 0, 0, 0], [0, 0, -1.0, 5.0], [0, 0, 0, 1.0] ])  
  robo.env.GetViewer().SetCamera(t)
    
  #robo.move_straight(1)
  #time.sleep(2)
    
  #robo.rotate_by(np.pi/2)
  #time.sleep(2)
  
  #robo.go_around_square()
  #time.sleep(2)
  
  #robo.figure_out_DOFS()
  #time.sleep(2)
  robo.put_in_self_collision()

  #from ipython import embedd
  # spin forever
  #while True:
  # time.sleep(1)