import numpy
import copy
from RRTTree import RRTTree

class RRTPlanner(object):

    def __init__(self, planning_env, visualize):
        self.planning_env = planning_env
        self.visualize = visualize
        

    def Plan(self, start_config, goal_config, epsilon = 0.5):
        
        tree = RRTTree(self.planning_env, start_config)
        plan = []
        self.plot = 0
        if self.visualize and hasattr(self.planning_env, 'InitializePlot'):
            self.planning_env.InitializePlot(goal_config)
        if (numpy.array_equal(self.planning_env.Extend(start_config,goal_config), goal_config)):
            plan.append(start_config)                    
            plan.append(goal_config)
            if self.plot:
                self.planning_env.PlotEdge(start_config, goal_config)
        else:
            plan.append(goal_config)
            while(1):
                conf = self.planning_env.GenerateRandomConfiguration()
                near_id, near_vert = tree.GetNearestVertex(conf)
                new_config = self.planning_env.Extend(near_vert,conf)
                if (new_config != None):
                    new_vert_id = tree.AddVertex(new_config)
                    tree.AddEdge(near_id, new_vert_id)                    
                    if self.plot:                    
                        self.planning_env.PlotEdge(near_vert, new_config)
                    if (self.planning_env.ComputeDistance(new_config,goal_config) < epsilon):
                        break
            plan.append(new_config)
            next_vert_id = copy.copy(new_vert_id)
            print next_vert_id
            while(1):
                next_vert_id = tree.edges[new_vert_id]
                print next_vert_id
                print tree.vertices[next_vert_id]
                plan.append(tree.vertices[next_vert_id])
                new_vert_id = next_vert_id
                print new_vert_id
                if (new_vert_id == 0):
                    break
            plan.reverse()
        old_vertex = plan[0]
        for i in range(1,len(plan)):
            new_vertex = plan[i]
            if self.plot:
                self.planning_env.PlotEdge(old_vertex, new_vertex,1)
            old_vertex = new_vertex
        print "Final Plan"
        print plan

        print "Number of Vertices"
        print len(tree.vertices)
        return plan