//*****************************************************************
//  MovingTarget1.h
//  Planning Learning and Execution
//  Assignment 2
//
//  Created by Abhishek Bhatia.
//
//  This header file contains the MovingTarget1 class declaration.
//*****************************************************************

#include <bits/stdc++.h>
using namespace std;

#define DEBUG 0

//*****************************************************************
// MovingTarget1 Class
//*****************************************************************
class CompareDist
{
public:
    bool operator()(pair<pair<int, int>,int> n1,pair<pair<int, int>,int> n2) {
        return n1.second>n2.second;
    }
};

class CompareDist2
{
public:
    bool operator()(pair<pair<int, int>,pair<int, int>> n1,pair<pair<int, int>,pair<int, int>> n2) {
        return n1.second.first > n2.second.first;
    }
};

class MovingTarget1
{
private:
    
public:
    int nodes_expanded = 0;
    float execution_time = 0;
    int cost_path = 0;

    int n; // width/height of the grid
    pair<int, int> r_init; // initial position of the robot
    pair<int, int> current; // current position of the robot
    pair<int, int> goal; // goal location
    vector<pair<int, int>> tar_pos; // position of the target at various timesteps
    vector<vector<int>> cost; // cost of every cell in the grid
    stack<pair<pair<int, int>, int>> final_path; // data structure to store the final path
    map<pair<int, int>, pair<int, int>> parent; // data structure to store the parent of every successor
    set<pair<int, int>> visited; // data structure to store the visited nodes / closed list
    priority_queue<pair<pair<int, int>, int>, vector<pair<pair<int, int>, int>>, CompareDist> q_astar; // priority queue for open list
    map<pair<int, int>, int> g_val; // data structure to store g values for every node
    map<pair<int, int>, int> gf_val;
    
    pair<int, int> pair_from_string(string str); // method to convert input string to an integer pair
    vector<int> vector_from_string(string str); // method to convert input string to an integer vector
    int myint(string str); // method to convert input string to integer
    void parse(char* input); // method to parse input file
    void wAstar(); // Weighted Astar for non-optimal planner that is computationally faster, at the expense of the optimality of the solution path computed
    int GenerateSuccesors(pair<int, int> loc); // method to generate succesors for the non - optimal planner
    int heu(pair<int, int> current, pair<int, int> ms); // method to computer heuristics for the non - optimal planner
};

class MovingTarget2 : public MovingTarget1
{
private:

public:
    queue<pair<pair<int, int>, int>> final_path; // data structure to store the final path
    set<pair<pair<int, int>, int>> visited2; // data structure to store the visited nodes / closed list
    map<pair<pair<int, int>, int>, pair<pair<int, int>, int>> parent2; // data structure to store the parent of every successor
    priority_queue<pair<pair<int, int>, pair<int, int>>, vector<pair<pair<int, int>, pair<int, int>>>, CompareDist2> q_astar2; // priority queue for open list
    pair<pair<int, int>, pair<int, int>> curr; // current state of the robot

    void Dijkstras(); // method to generate costs for each node starting from (0,0), which are used as a heuristic in the backwards A* search
    void GenerateSuccesorsF(pair<int, int> loc); //method to generate succesors while forward Dijkstra's search
    void GenerateSuccesorsB(pair<pair<int, int>, pair<int, int>> node_in); // method to generate succesors during backward A* search
    void BAstar(); // method for backwards A* search, planner that computes the least cost path that allows the robot to catch the moving target
};

//*****************************************************************
// End of File
//*****************************************************************