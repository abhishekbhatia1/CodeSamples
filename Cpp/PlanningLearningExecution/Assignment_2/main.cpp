//*****************************************************************
//  main.cpp
//  Planning Learning and Execution
//  Assignment 2
//
//  Created by Abhishek Bhatia.
//
//  This is the main source file.
//**************************************************************

#include "MovingTarget.cpp"

int main(int argc, char** argv)
{
    char* input;
    int planner;
    int testcase;
    
    //read input filename from command line
    if ( (argc <= 2) || (argv[argc-1] == NULL) ) {
        cout << "Incorrect arguments provided. Usage: ./main planner#(1/2) ProblemFile" << endl;
        return 0;
    }
    else {
        input = argv[argc-1];
        planner = atoi(argv[argc-2]);
    }
    
    //create an object of the MovingTarget class corresponding to the plannerresentation chosen
    if (planner == 1) {
        MovingTarget1 solution;
        cout << "Planner: Non Optimal, but computationally faster.\n";

        solution.execution_time = clock();
        solution.parse(input);
        solution.wAstar();
        solution.execution_time = (clock() - solution.execution_time)/double(CLOCKS_PER_SEC)*1000;

        cout << "Execution Time: " << solution.execution_time << " msecs" << endl;
        cout << "Number of nodes expanded: " << solution.nodes_expanded << endl;
        cout << "Cost of the path: " << solution.cost_path << endl;
        
        if (DEBUG) {
            cout << solution.n << endl;
            cout << solution.r_init.first << ", " << solution.r_init.second << endl;

            for (int i = 0; i < solution.tar_pos.size(); i++) {
                cout << solution.tar_pos[i].first << ", " << solution.tar_pos[i].second << endl;
            }

            for (int i = 0; i < solution.cost.size(); i++) {
                for (int j = 0; j < solution.cost.size(); j++) {
                    cout << solution.cost[i][j] << " ";
                }
                cout << endl;
            }
        }
    } 
    else if (planner == 2) {
        MovingTarget2 solution;
        cout << "Planner: Computationally slower, but optimal.\n";

        solution.execution_time = clock();
        solution.parse(input);
        solution.Dijkstras();
        solution.BAstar();
        solution.execution_time = (clock() - solution.execution_time)/double(CLOCKS_PER_SEC)*1000;

        cout << "Execution Time: " << solution.execution_time << " msecs" << endl;
        cout << "Number of nodes expanded: " << solution.nodes_expanded << endl;
        cout << "Cost of the path: " << solution.cost_path << endl;

        if (DEBUG) {
            cout << solution.n << endl;
            cout << solution.r_init.first << ", " << solution.r_init.second << endl;

            for (int i = 0; i < solution.tar_pos.size(); i++) {
                cout << solution.tar_pos[i].first << ", " << solution.tar_pos[i].second << endl;
            }

            for (int i = 0; i < solution.cost.size(); i++) {
                for (int j = 0; j < solution.cost.size(); j++) {
                    cout << solution.cost[i][j] << " ";
                }
                cout << endl;
            }
        }
    }
    else {
        cout << "Incorrect plannerresentation Entered.\n";
        return 0;
    }

    return 0;
}