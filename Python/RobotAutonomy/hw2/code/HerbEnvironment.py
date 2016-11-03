import numpy
import IPython
import math
import matplotlib.pyplot as pl
import copy
import random
import time

class HerbEnvironment(object):
    
    def __init__(self, herb):
        self.robot = herb.robot

        # add a table and move the robot into place
        table = self.robot.GetEnv().ReadKinBodyXMLFile('models/objects/table.kinbody.xml')
        self.robot.GetEnv().Add(table)

        table_pose = numpy.array([[ 0, 0, -1, 0.6], 
                                  [-1, 0,  0, 0], 
                                  [ 0, 1,  0, 0], 
                                  [ 0, 0,  0, 1]])
        table.SetTransform(table_pose)

        # set the camera
        camera_pose = numpy.array([[ 0.3259757 ,  0.31990565, -0.88960678,  2.84039211],
                                   [ 0.94516159, -0.0901412 ,  0.31391738, -0.87847549],
                                   [ 0.02023372, -0.9431516 , -0.33174637,  1.61502194],
                                   [ 0.        ,  0.        ,  0.        ,  1.        ]])
        self.robot.GetEnv().GetViewer().SetCamera(camera_pose)
        
        # goal sampling probability
        self.p = 0.0

    def SetGoalParameters(self, goal_config, p = 0.2):
        self.goal_config = goal_config
        self.p = p
        

    def GenerateRandomConfiguration(self):
        DOF_num=len(self.robot.GetActiveDOFIndices())
        lower_limits, upper_limits = self.robot.GetActiveDOFLimits()
        config = [0] * DOF_num
        DOF_init = self.robot.GetActiveDOFValues()
        table = self.robot.GetEnv().GetKinBody('conference_table')
        
        if (random.random() < self.p):
            return self.goal_config
        
        for i in range(DOF_num):
            config[i]=numpy.random.uniform(lower_limits[i], upper_limits[i])
        self.robot.SetActiveDOFValues(config)
            
        #Detecting colliion between table and robot
        while (self.robot.GetEnv().CheckCollision(self.robot,table)):
            # Generating random configuration
            for i in range(DOF_num):
                config[i]=numpy.random.uniform(lower_limits[i], upper_limits[i])
            self.robot.SetActiveDOFValues(config)
        #Moving the robot to the initial configuration
        self.robot.SetActiveDOFValues(DOF_init)
        #
        # TODO: Generate and return a random configuration
        #
        return numpy.array(config)


    
    def ComputeDistance(self, start_config, end_config):
        num = len(start_config)
        sum = 0
        for i in range(num):
            sum =  sum + (start_config[i] - end_config[i])**2
        distance = math.sqrt(sum)
        return distance
	

        #
        # TODO: Implement a function which computes the distance between
        # two configurations
        #
    
    def Extend(self, start_config, end_config):
        table = self.robot.GetEnv().GetKinBody('conference_table')
        DOF_init = self.robot.GetActiveDOFValues()
        self.th = 0.1
        self.val = 0.1
        self.new_config = copy.copy(start_config)
        self.robot.SetActiveDOFValues(start_config)
        
        for j in range(10):
            if ((self.robot.GetEnv().CheckCollision(self.robot,table))==False and self.robot.GetEnv().CheckCollision(self.robot,self.robot)==False):
                self.old_config = copy.copy(self.new_config)
                self.new_config = numpy.add((1-self.val)*start_config, self.val*end_config)
                self.val = self.val + self.th;
                self.robot.SetActiveDOFValues(self.new_config)
            else:
                if (numpy.array_equal(self.new_config, start_config)):
                    return start_config
                else:
                    return self.old_config
                break
            
        self.robot.SetActiveDOFValues(DOF_init)    
        return self.old_config
        
        #
        # TODO: Implement a function which attempts to extend from 
        #   a start configuration to a goal configuration
        #
        
        
    def ShortenPath(self, path, timeout=5.0):
        short_path = []
        for conf in path:
            short_path.append(conf)
            if (numpy.array_equal(self.Extend(numpy.array(conf),numpy.array(path[len(path)-1])), numpy.array(path[len(path)-1]))):
                if (numpy.array_equal(numpy.array(conf), numpy.array(path[len(path)-1]))):
                    break
                short_path.append(path[len(path)-1])
        path = short_path
        self.val = 0.1
        table = self.robot.GetEnv().GetKinBody('conference_table')
        DOF_init = self.robot.GetActiveDOFValues()
        for ind in range(0,1):
            for i in range(0,len(path)-1):
                conf = path[i]
                trial_config = numpy.add((1-self.val)*numpy.array(conf), self.val*numpy.array(path[-1]))            
                self.robot.SetActiveDOFValues(trial_config)
                if ((self.robot.GetEnv().CheckCollision(self.robot,table))==False and self.robot.GetEnv().CheckCollision(self.robot,self.robot)==False):
                #if ((self.robot.GetEnv().CheckCollision(self.robot,table))==False):
                    path[i] = trial_config
                    '''                    
                    if (i-1 < 0):
                        if (numpy.array_equal(self.Extend(numpy.array(trial_config),numpy.array(path[i+1])), numpy.array(path[i+1]))):
                            path[i] = trial_config
                    elif (i+1 > len(path)-1):
                        if (numpy.array_equal(self.Extend(numpy.array(trial_config),numpy.array(path[i-1])), numpy.array(path[i-1]))):
                            path[i] = trial_config
                    else:
                        if (numpy.array_equal(self.Extend(numpy.array(trial_config),numpy.array(path[i+1])), numpy.array(path[i+1])) and numpy.array_equal(self.Extend(numpy.array(trial_config),numpy.array(path[i-1])), numpy.array(path[i-1]))):
                            path[i] = trial_config
                    '''
        self.robot.SetActiveDOFValues(DOF_init)
        print "Final Shorten Path"
        print path
        return path
        '''
        #print "shortening path"
        if (type(path[0]) == numpy.ndarray):
            path[0] = path[0].tolist()
        if (type(path[-1]) == numpy.ndarray):
            path[-1] = path[-1].tolist()
        #print path

        startTime = time.time()
        old_path = []
        goal_conf = path[len(path)-1]

        # Remove redundant points
        for i in range(0,len(path)-2):
            if (i >= len(path)):
                break
            conf = path[i]
            for j in range(i+2,len(path)):
                if (j >= len(path)):
                    break
                if (path[j] == None):
                    path.remove(path[j])
                if numpy.array_equal(self.Extend(numpy.array(conf),numpy.array(path[j])), numpy.array(path[j])):
                #if (self.Extend(conf,path[j]) == path[j]):
                    path.remove(path[j-1])
                    if (j>=len(path)):
                        break
        
        while ((old_path != path) & (time.time() < startTime+timeout)):
            #print "Made it into loop"
            #print startTime+timeout-time.time()
            print time.time()
            old_path = path

            # Add extra points between each existing point
            new_path = []
            for i in range(0,len(path)-1):
                new_configs = []
                # new_path.append(path[i])
                linDof = []
                self.th = 0.2
                self.val = 0.2
                self.new_config = copy.copy(path[i])
                self.robot.SetActiveDOFValues(path[i])
                table = self.robot.GetEnv().GetKinBody('conference_table')
                for j in range(5):
                    if ((self.robot.GetEnv().CheckCollision(self.robot,table))==False and self.robot.GetEnv().CheckCollision(self.robot,self.robot)==False):
                        self.old_config = copy.copy(self.new_config)
                        self.new_config = numpy.add((1-self.val)*numpy.array(path[i]), self.val*numpy.array(path[i+1]))
                        self.val = self.val + self.th;
                        linDof.append(self.new_config)
                    else:
                        continue
                #for j in range(0,len(path[i])):
                #    linDof.append(numpy.linspace(path[i][j],path[i+1][j],2))
                print "linDof: "
                print linDof
                for conf in linDof:
                    new_path.append(conf)
                    
            path = new_path
            print "new_path: "
            print new_path

            # Remove redundant points
            for i in range(0,len(path)-2):
                if (i >= len(path)):
                    break
                conf = path[i]

                for j in range(i+2,len(path)):
                    if (j >= len(path)):
                        break
                    if (path[j] == None):
                        path.remove(path[j])
                    #if (self.Extend(conf,path[j]) == path[j]):
                    if numpy.array_equal(self.Extend(numpy.array(conf),numpy.array(path[j])), numpy.array(path[j])):
                        path.remove(path[j-1])
                        if time.time() >= startTime+timeout:
                            old_path.append(goal_conf)
                            print "Final Shorten Path"
                            print old_path
                            return old_path
                        if (j>=len(path)):
                            break
        path.append(goal_conf)                    
        print "Final Shorten Path"
        print path
        return path
        '''