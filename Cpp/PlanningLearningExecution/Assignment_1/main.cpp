//*****************************************************************
//  main.cpp
//  Planning Learning and Execution
//  Assignment 1
//
//  Created by Abhishek Bhatia.
//
//  This is the main source file.
//**************************************************************

#include "GamePlay.cpp"

int main(int argc, char** argv)
{
    char* input;
    int rep;
    
    //read input filename from command line
    if ( (argc <= 2) || (argv[argc-1] == NULL) ) {
        cout << "Incorrect arguments provided. Usage: ./main Representation#(1/2) ProblemFile" << endl;
        return 0;
    }
    else {
        input = argv[argc-1];
        rep = atoi(argv[argc-2]);
    }
    
    //create an object of the GamePlay class corresponding to the representation chosen
    if (rep == 1) {
        GamePlay1 solution;
        solution.parse1(input);
        solution.BFS(solution.initial_state);
        solution.print_path(solution.initial_state);
    } 
    else if (rep == 2) {
        GamePlay2 solution;
        solution.parse2(input);
        solution.BFS(solution.initial_state);
        solution.print_path(solution.initial_state);
    }
    else {
        cout << "Incorrect Representation Entered.\n";
        return 0;
    }

    return 0;
}