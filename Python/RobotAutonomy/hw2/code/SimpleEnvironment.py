import numpy
import matplotlib.pyplot as pl
import IPython
import math
import copy
import random
import time

class SimpleEnvironment(object):
    
    def __init__(self, herb):
        self.robot = herb.robot
        self.boundary_limits = [[-5., -5.], [5., 5.]]

        # add an obstacle
        table = self.robot.GetEnv().ReadKinBodyXMLFile('models/objects/table.kinbody.xml')
        self.robot.GetEnv().Add(table)

        table_pose = numpy.array([[ 0, 0, -1, 1.0], 
                                  [-1, 0,  0, 0], 
                                  [ 0, 1,  0, 0], 
                                  [ 0, 0,  0, 1]])
        table.SetTransform(table_pose)
        
        #self.rand_config1 = self.GenerateRandomConfiguration()
        #self.rand_config2 = self.GenerateRandomConfiguration()
        #self.ComputeDistance(self.rand_config1, self.rand_config2)
        #print self.robot.GetTransform()
        #print self.Extend([0,0],[1,-0.8])

        # goal sampling probability
        self.p = 0.0

    def SetGoalParameters(self, goal_config, p = 0.2):
        self.goal_config = goal_config
        self.p = p
        
    def GenerateRandomConfiguration(self):
        config = [0] * 2;
        lower_limits, upper_limits = self.boundary_limits
        
        if (random.random() < self.p):
            return self.goal_config
        
        #Generating Random Configuration
        config[0] = numpy.random.uniform(lower_limits[0],upper_limits[0])
        config[1] = numpy.random.uniform(lower_limits[1],upper_limits[1])
        
        #Moving Robot to generated Configuration
        tf_init = self.robot.GetTransform()
        tf_new = numpy.array([[ 1, 0, 0, config[0]], 
                              [ 0, 1, 0, config[1]], 
                              [ 0, 0, 1, 0], 
                              [ 0, 0, 0, 1]])
        self.robot.SetTransform(tf_new)
        
        #Generating Table's Configuration
        table = self.robot.GetEnv().GetKinBody('conference_table')
        
        #Detecting collision between Table's Configuration and Robot's Configuration
        #The config point generated once this while loop exits is collision free
        while ((self.robot.GetEnv().CheckCollision(self.robot,table))):
            config[0] = numpy.random.uniform(lower_limits[0],upper_limits[0])
            config[1] = numpy.random.uniform(lower_limits[1],upper_limits[1])
            tf_new = numpy.array([[ 1, 0, 0, config[0]], 
                                  [ 0, 1, 0, config[1]], 
                                  [ 0, 0, 1, 0], 
                                  [ 0, 0, 0, 1]])
            self.robot.SetTransform(tf_new)
        
        #Moving Robot to Initial Configuration
        self.robot.SetTransform(tf_init)
        
        #Returning collision free configuration
        return numpy.array(config)

    def ComputeDistance(self, start_config, end_config):
        distance = math.sqrt((start_config[0] - end_config[0])**2 + (start_config[1] - end_config[1])**2)
        #print distance
        return distance

    def Extend(self, start_config, end_config):
        table = self.robot.GetEnv().GetKinBody('conference_table')
        lin_x = numpy.linspace(start_config[0], end_config[0],50)
        a = start_config
        b = end_config
        if (b[0] != a[0]):
            m = float(float(b[1]-a[1])/float(b[0]-a[0]))
            lin_y = (a[1]) + (m*(lin_x-a[0]))
        else:
            lin_y = numpy.linspace(start_config[1], end_config[1],50)
        tf_init = self.robot.GetTransform()
        config_past = start_config    
        lin_config = [0]*2
        
        for i in range(1,len(lin_x)):
            lin_config[0] = lin_x[i]
            lin_config[1] = lin_y[i]
            tf_new = numpy.array([[ 1, 0, 0, lin_config[0]], 
                                  [ 0, 1, 0, lin_config[1]], 
                                  [ 0, 0, 1, 0], 
                                  [ 0, 0, 0, 1]])
            self.robot.SetTransform(tf_new)
            if (self.robot.GetEnv().CheckCollision(self.robot,table)):
                if(numpy.array_equal(config_past, start_config)):
                    return start_config
                else:
                    return config_past
            config_past = copy.copy(lin_config)
        
        self.robot.SetTransform(tf_init)
        #print config_past
        return config_past

    def ShortenPath(self, path, timeout=5.0):
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
                if (self.Extend(conf,path[j]) == path[j]):
                    path.remove(path[j-1])
                    if (j>=len(path)):
                        break

        while ((old_path != path) & (time.time() < startTime+timeout)):
            #print "Made it into loop"
            #print startTime+timeout-time.time()
            old_path = path

            # Add extra points between each existing point
            new_path = []
            for i in range(0,len(path)-1):
                new_configs = []
                # new_path.append(path[i])
                linDof = []
                for j in range(0,len(path[i])):
                    linDof.append(numpy.linspace(path[i][j],path[i+1][j],6))
                for j in range(0,len(linDof[0])-1):
                    new_config = []
                    for k in range(0,len(linDof)):
                        new_config.append(linDof[k][j])
                    new_configs.append(new_config)
                for conf in new_configs:
                    new_path.append(conf)

            path = new_path
            #print new_path

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
                    if (self.Extend(conf,path[j]) == path[j]):
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


    def InitializePlot(self, goal_config):
        self.fig = pl.figure()
        lower_limits, upper_limits = self.boundary_limits
        pl.xlim([lower_limits[0], upper_limits[0]])
        pl.ylim([lower_limits[1], upper_limits[1]])
        pl.plot(goal_config[0], goal_config[1], 'gx')

        # Show all obstacles in environment
        for b in self.robot.GetEnv().GetBodies():
            if b.GetName() == self.robot.GetName():
                continue
            bb = b.ComputeAABB()
            pl.plot([bb.pos()[0] - bb.extents()[0],
                     bb.pos()[0] + bb.extents()[0],
                     bb.pos()[0] + bb.extents()[0],
                     bb.pos()[0] - bb.extents()[0],
                     bb.pos()[0] - bb.extents()[0]],
                    [bb.pos()[1] - bb.extents()[1],
                     bb.pos()[1] - bb.extents()[1],
                     bb.pos()[1] + bb.extents()[1],
                     bb.pos()[1] + bb.extents()[1],
                     bb.pos()[1] - bb.extents()[1]], 'r')
                    
                     
        pl.ion()
        pl.show()
        
    def PlotEdge(self, sconfig, econfig, col=0):
        if (sconfig != None and econfig != None):
            if (col == 0):
                pl.plot([sconfig[0], econfig[0]],
                        [sconfig[1], econfig[1]],
                        'k.-', linewidth=2.5)
            elif (col == 1):
                pl.plot([sconfig[0], econfig[0]],
                        [sconfig[1], econfig[1]],
                        'k.-', linewidth=2.5, color='r')
            elif (col == 2):
                pl.plot([sconfig[0], econfig[0]],
                        [sconfig[1], econfig[1]],
                        'k.-', linewidth=2.5, color='b')
            elif (col == 3):
                pl.plot([sconfig[0], econfig[0]],
                        [sconfig[1], econfig[1]],
                        'k.-', linewidth=2.5, color='y')            
            else:
                pl.plot([sconfig[0], econfig[0]],
                        [sconfig[1], econfig[1]],
                        'k.-', linewidth=2.5, color='g')
        pl.draw()

