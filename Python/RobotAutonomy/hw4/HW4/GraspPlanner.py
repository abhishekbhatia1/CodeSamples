# Standard Python Imports
import os
import copy
import time
import math
import numpy as np
np.random.seed(0)
import scipy
import scipy.stats

import logging, openravepy

class GraspPlanner(object):

    def __init__(self, robot, base_planner, arm_planner):
        self.robot = robot
        self.base_planner = base_planner
        self.arm_planner = arm_planner

            
    def GetBasePoseForObjectGrasp(self, obj):

        # Load grasp database
        gmodel = openravepy.databases.grasping.GraspingModel(self.robot, obj)
        if not gmodel.load():
            gmodel.autogenerate()

        base_pose = None
        grasp_config = None
       
        ###################################################################
        # TODO: Here you will fill in the function to compute
        #  a base pose and associated grasp config for the 
        #  grasping the bottle
        ###################################################################

        # Generating Grasp Config

        # create a grasping module
        self.gmodel = openravepy.databases.grasping.GraspingModel(self.robot, obj)

        # if you want to set options, e.g. friction
        options = openravepy.options
        options.friction = 0.1
        if not self.gmodel.load():
          self.gmodel.autogenerate(options)

        self.graspindices = self.gmodel.graspindices
        self.grasps = self.gmodel.grasps

        print 'Computing Grasps'
        self.order_grasps()
        
        initial_config = self.base_planner.planning_env.herb.GetCurrentConfiguration()
        '''
        # Test Case 1
        bp = np.array([[1, 0, 0, -0.15],
                          [0, 1, 0,  0],
                          [0, 0, 1,  0],
                          [0, 0, 0,  1]])
        
        #Test Case 2
        bp = np.array([[1, 0, 0, -0.15],
                          [0, 1, 0,  -0.55],
                          [0, 0, 1,  0],
                          [0, 0, 0,  1]])
        '''
        #Test Case 3
        bp = np.array([[-1, 0, 0, 1.5],
                          [0, -1, 0,  0.5],
                          [0, 0, 1,  0],
                          [0, 0, 0,  1]])
        

        self.base_planner.planning_env.herb.robot.SetTransform(bp)
        grasp_pose_in_world = gmodel.getGlobalGraspTransform(self.grasps_ordered[0], collisionfree = True)

        # Determining Base Pose
        #self.irmodel = openravepy.databases.inversereachability.InverseReachabilityModel(robot=self.robot)
        #self.irmodel.load()
        #densityfn,samplerfn,bounds = self.irmodel.computeBaseDistribution(grasp_pose_in_world)
        #print bounds

        # initialize sampling parameters
        '''
        goals = []
        numfailures = 0
        starttime = time.time()
        timeout = float('inf')
        with self.robot:
            N = 10
            while len(goals) < N:
                if time.time()-starttime > timeout:
                    break
                poses,jointstate = samplerfn(N-len(goals))
                for pose in poses:
                    self.base_planner.planning_env.herb.robot.SetTransform(pose)
                    self.base_planner.planning_env.herb.robot.SetDOFValues(*jointstate)
                    # validate that base is not in collision
                    if not self.arm_planner.planning_env.herb.manip.CheckIndependentCollision(openravepy.CollisionReport()):
                        q = self.arm_planner.planning_env.herb.manip.FindIKSolution(grasp_pose_in_world,filteroptions=openravepy.IkFilterOptions.CheckEnvCollisions)
                        if q is not None:
                            values = self.base_planner.planning_env.herb.robot.GetDOFValues()
                            values[self.arm_planner.planning_env.herb.manip.GetArmIndices()] = q
                            goals.append((grasp_pose_in_world,pose,values))
                        elif self.arm_planner.planning_env.herb.manip.FindIKSolution(grasp_pose_in_world,0) is None:
                            numfailures += 1
        '''

        #self.base_planner.planning_env.herb.robot.SetTransform(bp)
        grasp_config = self.arm_planner.planning_env.herb.manip.FindIKSolution(grasp_pose_in_world, filteroptions = openravepy.IkFilterOptions.CheckEnvCollisions)
        print 'Grasp Config: '
        print grasp_config

        ip_th = initial_config[2]
        ip = np.array([[np.cos(ip_th), -np.sin(ip_th), 0, initial_config[0]],
                          [np.sin(ip_th), np.cos(ip_th), 0,  initial_config[1]],
                          [0, 0, 1,  0   ],
                          [0, 0, 0,  1.  ]])
        self.base_planner.planning_env.herb.robot.SetTransform(ip)

        # Test Case 1
        #base_pose = np.array([-0.15,0,0]);

        #Test Case 2
        #base_pose = np.array([-0.15,-0.55,0]);

        #Test Case 2
        base_pose = np.array([1.5,0.5,np.pi]);

        print 'Base Pose: '
        print base_pose
        
        return base_pose, grasp_config

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
        
        for grasp in self.grasps_ordered:
            net_score = 800*s1_list[i] + 100*s2_list[i] + 200*s3_list[i]
            grasp[self.graspindices.get('performance')] = net_score
            i += 1
  
        # sort!
        order = np.argsort(self.grasps_ordered[:,self.graspindices.get('performance')[0]])
        order = order[::-1]
        self.grasps_ordered = self.grasps_ordered[order]

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
            
            score1 = np.sqrt(abs(np.linalg.det(np.dot(G, np.transpose(G)))))
            
            #Metric = Ratio of sigmamax and sigmamin
            U, s, V = np.linalg.svd(G, full_matrices = True)
            sig_max = s[0]
            sig_min = s[len(s)-1]
            score2 = sig_min/sig_max
            score3 = sig_min
            return score1, score2, score3

          except openravepy.planning_error,e:
            #you get here if there is a failure in planning
            #example: if the hand is already intersecting the object at the initial position/orientation
            print 'Bad Grasp, score = 0'

            return  0,0,0 # TODO you may want to change this

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

    def PlanToGrasp(self, obj):

        # Next select a pose for the base and an associated ik for the arm
        base_pose, grasp_config = self.GetBasePoseForObjectGrasp(obj)

        if base_pose is None or grasp_config is None:
            print 'Failed to find solution'
            exit()

        # Now plan to the base pose
        start_pose = np.array(self.base_planner.planning_env.herb.GetCurrentConfiguration())
        base_plan = self.base_planner.Plan(start_pose, base_pose)
        base_traj = self.base_planner.planning_env.herb.ConvertPlanToTrajectory(base_plan)

        print 'Executing base trajectory'
        self.base_planner.planning_env.herb.ExecuteTrajectory(base_traj)

        # Now plan the arm to the grasp configuration
        start_config = np.array(self.arm_planner.planning_env.herb.GetCurrentConfiguration())
        arm_plan = self.arm_planner.Plan(start_config, grasp_config)
        arm_traj = self.arm_planner.planning_env.herb.ConvertPlanToTrajectory(arm_plan)

        print 'Executing arm trajectory'
        self.arm_planner.planning_env.herb.ExecuteTrajectory(arm_traj)

        # Grasp the bottle
        task_manipulation = openravepy.interfaces.TaskManipulation(self.robot)
        task_manipulation.CloseFingers()
        
    
