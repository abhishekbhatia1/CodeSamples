#!/usr/bin/env python

PACKAGE_NAME = 'hw1'

# Standard Python Imports
import os
import copy
import time
import math
import numpy as np
np.random.seed(0)
import scipy
import scipy.stats

# OpenRAVE
import openravepy
#openravepy.RaveInitialize(True, openravepy.DebugLevel.Debug)


curr_path = os.getcwd()
relative_ordata = '/models'
ordata_path_thispack = curr_path + relative_ordata


#this sets up the OPENRAVE_DATA environment variable to include the files we're using
openrave_data_path = os.getenv('OPENRAVE_DATA', '')
openrave_data_paths = openrave_data_path.split(':')
if ordata_path_thispack not in openrave_data_paths:
  if openrave_data_path == '':
      os.environ['OPENRAVE_DATA'] = ordata_path_thispack
  else:
      datastr = str('%s:%s'%(ordata_path_thispack, openrave_data_path))
      os.environ['OPENRAVE_DATA'] = datastr

#set database file to be in this folder only
relative_ordatabase = '/database'
ordatabase_path_thispack = curr_path + relative_ordatabase
os.environ['OPENRAVE_DATABASE'] = ordatabase_path_thispack

#get rid of warnings
openravepy.RaveInitialize(True, openravepy.DebugLevel.Fatal)
openravepy.misc.InitOpenRAVELogging()



class RoboHandler:
  def __init__(self):
    self.openrave_init()
    self.problem_init()

    
    #order grasps based on your own scoring metric
    #Comment/Uncomment this code to run order_grasps function
    print 'Computing Grasps'
    self.order_grasps()
    val = 0
    while val >= 0:
      try:
        val = int(raw_input("Show Grasp (Insert index): "))
        if val >= 0:
          self.show_grasp(self.grasps_ordered[val])
      except:
        print "Invalid"

    #order grasps with noise
    #Comment/Uncomment this code to run order_grasps_noisy function
    #print 'Computing Noisy Grasps'
    #self.order_grasps_noisy()
    #val = 0
    #while val >= 0:
    #  try:
    #    val = int(raw_input("Show Noisy Grasp (Insert index): "))
    #    if val >= 0:
    #      self.show_grasp(self.grasps_ordered_noisy[val])
    #  except:
    #    print "Invalid"


  # the usual initialization for openrave
  def openrave_init(self):
    self.env = openravepy.Environment()
    self.env.SetViewer('qtcoin')
    self.env.GetViewer().SetName('HW1 Viewer')
    self.env.Load('models/%s.env.xml' %PACKAGE_NAME)
    # time.sleep(3) # wait for viewer to initialize. May be helpful to uncomment
    self.robot = self.env.GetRobots()[0]
    self.manip = self.robot.GetActiveManipulator()
    self.end_effector = self.manip.GetEndEffector()

  # problem specific initialization - load target and grasp module
  def problem_init(self):
    self.target_kinbody = self.env.ReadKinBodyURI('models/objects/champagne.iv')
    #self.target_kinbody = self.env.ReadKinBodyURI('models/objects/winegoblet.iv')
    #self.target_kinbody = self.env.ReadKinBodyURI('models/objects/black_plastic_mug.iv')

    #change the location so it's not under the robot
    T = self.target_kinbody.GetTransform()
    T[0:3,3] += np.array([0.5, 0.5, 0.5])
    self.target_kinbody.SetTransform(T)
    self.env.AddKinBody(self.target_kinbody)

    # create a grasping module
    self.gmodel = openravepy.databases.grasping.GraspingModel(self.robot, self.target_kinbody)
    
    # if you want to set options, e.g. friction
    options = openravepy.options
    options.friction = 0.1
    if not self.gmodel.load():
      self.gmodel.autogenerate(options)

    self.graspindices = self.gmodel.graspindices
    self.grasps = self.gmodel.grasps

  
  # order the grasps - call eval grasp on each, set the 'performance' index, and sort
  def order_grasps(self):
    self.grasps_ordered = self.grasps.copy() #you should change the order of self.grasps_ordered
    s1_list = []
    s2_list = []
    s3_list  = []
    for grasp in self.grasps_ordered:
      s1, s2, s3 = self.eval_grasp(grasp)
      s1_list.append(s1)
      s2_list.append(s2)
      s3_list.append(s3)
    s1_list[:] = [x/max(s1_list) for x in s1_list]
    s2_list[:] = [x/max(s2_list) for x in s2_list]
    s3_list[:] = [x/max(s3_list) for x in s3_list] 
    i = 0
    
    #for index in range(len(s1_list)-1):
    #    print s1_list[index]
    
    for grasp in self.grasps_ordered:
    	net_score = 800*s1_list[i] + 100*s2_list[i] + 200*s3_list[i]
    	grasp[self.graspindices.get('performance')] = net_score
    	i += 1

      
    # sort!
    order = np.argsort(self.grasps_ordered[:,self.graspindices.get('performance')[0]])
    order = order[::-1]
    self.grasps_ordered = self.grasps_ordered[order]
    #for grasp in self.grasps_ordered:
    #    print grasp[self.graspindices.get('performance')]
    #    #print grasp

    
    #for grasp in self.grasps_ordered:
    #self.show_grasp(self.grasps_ordered[2])
    #self.show_grasp(grasp)
    #while True:
    #time.sleep(1)

  
  # order the grasps - but instead of evaluating the grasp, evaluate random perturbations of the grasp 
  def order_grasps_noisy(self):
    self.grasps_ordered_noisy = self.grasps.copy() #you should change the order of self.grasps_ordered_noisy
    #TODO set the score with your evaluation function (over random samples) and sort
    
    NUM_NOISY_GRASPS = 10 #Number of randomly perturbed graps to try
    s1_list = []
    s2_list = []
    s3_list  = []    
    
    for random_grasp in self.grasps_ordered_noisy:        
        #score = self.eval_grasp(random_grasp)
        s1, s2, s3 = self.eval_grasp(random_grasp)

        #Perturb grasp x number of times
        for i in range(NUM_NOISY_GRASPS):
          noisy_grasp,P = self.sample_random_grasp(random_grasp) #Perturb grasp
          if P > 0:
            #score += self.eval_grasp(noisy_grasp) * P #Evaluate grasp performance
            s1, s2, s3 = self.eval_grasp(noisy_grasp)
            #Evaluate grasp performance
            s1 = s1 + s1 * P
            s2 = s2 + s2 * P
            s3 = s3 + s3 * P
        
        s1 /= NUM_NOISY_GRASPS
        s2 /= NUM_NOISY_GRASPS
        s3 /= NUM_NOISY_GRASPS
        s1_list.append(s1)
        s2_list.append(s2)
        s3_list.append(s3)
        
        #print 'Score = '+repr(score)
        #random_grasp[self.graspindices.get('performance')] = score
    	
    s1_list[:] = [x/max(s1_list) for x in s1_list]
    s2_list[:] = [x/max(s2_list) for x in s2_list]
    s3_list[:] = [x/max(s3_list) for x in s3_list] 
    i = 0
    
    for random_grasp in self.grasps_ordered_noisy:
    	net_score = 800*s1_list[i] + 100*s2_list[i] + 200*s3_list[i]
    	random_grasp[self.graspindices.get('performance')] = net_score
    	i += 1

    #sort
    order_noisy = np.argsort(self.grasps_ordered_noisy[:,self.graspindices.get('performance')[0]])
    order_noisy = order_noisy[::-1]
    self.grasps_ordered_noisy = self.grasps_ordered_noisy[order_noisy]

    #for random_grasp in self.grasps_ordered_noisy:
    #    self.show_grasp(random_grasp)
    for random_grasp in self.grasps_ordered_noisy:
        print random_grasp[self.graspindices.get('performance')]
    self.show_grasp(self.grasps_ordered_noisy[0])
    #self.show_grasp(self.grasps_ordered[len(order) - 1])
    #while True:
    #time.sleep(1)


  # function to evaluate grasps
  # returns a score, which is some metric of the grasp
  # higher score should be a better grasp
  # function to evaluate grasps
  # returns a score, which is some metric of the grasp
  # higher score should be a better grasp
  def eval_grasp(self, grasp):
    with self.robot:
      #contacts is a 2d array, where contacts[i,0-2] are the positions of contact i and contacts[i,3-5] is the direction
      try:
        contacts,finalconfig,mindist,volume = self.gmodel.testGrasp(grasp=grasp,translate=True,forceclosure=False)
        
        obj_position = self.gmodel.target.GetTransform()[0:3,3]
        # for each contact
        
        G = np.array([]) #the wrench matrix
        scores = np.array([])
        
        if len(contacts) <= 1:
          return 0,0,0

        for c in contacts:
          pos = c[0:3] - obj_position
          dir = -c[3:] #this is already a unit vector
          t = np.cross(dir,pos)
          col = np.hstack([pos,np.cross(pos,dir)])      
          
          if len(G) == 0:
          	G = np.append(G,col)
          else:
          	G = np.vstack([G,col])

        G = np.transpose(G)	
        #print G.shape 
        
        #print "G transpose ", np.transpose(G)
        #print "Determinant ", np.linalg.det(np.dot(np.transpose(G), G))
        #TODO use G to compute scores as discussed in class
        
        #Metric = Volume of ellipsoid
        score1 = np.sqrt(abs(np.linalg.det(np.dot(G, np.transpose(G)))))
        
        #Metric = Ratio of sigmamax and sigmamin
        U, s, V = np.linalg.svd(G, full_matrices = True)
        sig_max = s[0]
        sig_min = s[len(s)-1]
        score2 = sig_min/sig_max
        score3 = sig_min
        #print "score = ", score
        #change this
        return score1, score2, score3

      except openravepy.planning_error,e:
        #you get here if there is a failure in planning
        #example: if the hand is already intersecting the object at the initial position/orientation
        print 'Bad Grasp, score = 0'

        return  0,0,0 # TODO you may want to change this
      
      #heres an interface in case you want to manipulate things more specifically
      #NOTE for this assignment, your solutions cannot make use of graspingnoise
#      self.robot.SetTransform(np.eye(4)) # have to reset transform in order to remove randomness
#      self.robot.SetDOFValues(grasp[self.graspindices.get('igrasppreshape')], self.manip.GetGripperIndices())
#      self.robot.SetActiveDOFs(self.manip.GetGripperIndices(), self.robot.DOFAffine.X + self.robot.DOFAffine.Y + self.robot.DOFAffine.Z)
#      self.gmodel.grasper = openravepy.interfaces.Grasper(self.robot, friction=self.gmodel.grasper.friction, avoidlinks=[], plannername=None)
#      contacts, finalconfig, mindist, volume = self.gmodel.grasper.Grasp( \
#            direction             = grasp[self.graspindices.get('igraspdir')], \
#            roll                  = grasp[self.graspindices.get('igrasproll')], \
#            position              = grasp[self.graspindices.get('igrasppos')], \
#            standoff              = grasp[self.graspindices.get('igraspstandoff')], \
#            manipulatordirection  = grasp[self.graspindices.get('imanipulatordirection')], \
#            target                = self.target_kinbody, \
#            graspingnoise         = 0.0, \
#            forceclosure          = True, \
#            execute               = False, \
#            outputfinal           = True, \
#            translationstepmult   = None, \
#            finestep              = None )



  # given grasp_in, create a new grasp which is altered randomly
  # you can see the current position and direction of the grasp by:
  # grasp[self.graspindices.get('igrasppos')]
  # grasp[self.graspindices.get('igraspdir')]
  def sample_random_grasp(self, grasp_in):
    grasp = grasp_in.copy()

    #sample random position
    RAND_DIST_SIGMA = 0.001 #TODO you may want to change this
    pos_orig = grasp[self.graspindices['igrasppos']]
    #TODO set a random position
    pos_new = np.random.normal(pos_orig,RAND_DIST_SIGMA)
    
    #sample random orientation
    RAND_ANGLE_SIGMA = np.pi/80 #TODO you may want to change this
    dir_orig = grasp[self.graspindices['igraspdir']]
    roll_orig = grasp[self.graspindices['igrasproll']]
    #TODO set the direction and roll to be random
    dir_new = np.random.normal(dir_orig,RAND_ANGLE_SIGMA)
    roll_new = np.random.normal(roll_orig,RAND_ANGLE_SIGMA)
    
    try:
        with self.env:
            grasp[self.graspindices['igrasppos']] = pos_new
            grasp[self.graspindices['igraspdir']] = dir_new
            grasp[self.graspindices['igrasproll']] = roll_new

            #Compute distance from original to perturbed position
            d_pos = np.linalg.norm(pos_orig - pos_new)
            d_dir = np.linalg.norm(dir_orig - dir_new)
            d_roll = np.linalg.norm(roll_orig - roll_new)

            #Weight each distance using the normal distribtution 
            P_pos = scipy.stats.norm(0,RAND_DIST_SIGMA).pdf(d_pos)
            P_dir = scipy.stats.norm(0,RAND_ANGLE_SIGMA).pdf(d_pos)
            P_roll = scipy.stats.norm(0,RAND_ANGLE_SIGMA).pdf(d_pos)

            #Compute total probability of grasp position
            P_total = P_pos*P_dir*P_roll

    except openravepy.planning_error,e:
        print 'intersecting grasp',e
        P_total = 0

    return grasp, P_total


  #displays the grasp
  def show_grasp(self, grasp, delay=10):
    with openravepy.RobotStateSaver(self.gmodel.robot):
      with self.gmodel.GripperVisibility(self.gmodel.manip):
        time.sleep(0.1) # let viewer update?
        try:
          with self.env:
            contacts,finalconfig,mindist,volume = self.gmodel.testGrasp(grasp=grasp,translate=True,forceclosure=True)
            #if mindist == 0:
            #  print 'grasp is not in force closure!'
            contactgraph = self.gmodel.drawContacts(contacts) if len(contacts) > 0 else None
            self.gmodel.robot.GetController().Reset(0)
            self.gmodel.robot.SetDOFValues(finalconfig[0])
            self.gmodel.robot.SetTransform(finalconfig[1])
            self.env.UpdatePublishedBodies()
            time.sleep(delay)
        except openravepy.planning_error,e:
          print 'bad grasp!',e

if __name__ == '__main__':
  robo = RoboHandler()
  #time.sleep(10000) #to keep the openrave window open

  
