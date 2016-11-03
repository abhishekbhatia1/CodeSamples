//*****************************************************************
//  main.cpp
//
//  Created by Abhishek Bhatia.
//
//  This is the main source file.
//**************************************************************

#include "KnightBoard.h"

int main(int argc, char** argv)
{
    char* input;
    int level;
    
    //read input filename from command line
    if ( (argc <= 2) || (argv[argc-1] == NULL) ) {
        cout << "Incorrect arguments provided. Usage: ./main InputFile Level" << endl;
        return 0;
    }
    else {
        input = argv[argc-2];
        level = atoi(argv[argc-1]);
    }
    
    if (level < 5) {
        
        KnightBoard solution;

        solution.parse(input);

        cout << "Input State:\n";
        solution.print_state(0);

        clock_t begin = clock();
        
        if (level == 1) 
            solution.level1_validMoves(solution.move_seqs);
        
        if (level == 2)
            solution.level2_computeValidMoves();

        if (level == 3)
            solution.level3_computeValidFewestMoves();

        if (level == 4)
            solution.level4_computeValidFewestMoves();

        cout << "Final State:\n";
        solution.print_state(1);

        clock_t end = clock();
        double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;

        if (level == 2)
            cout << "BFS took: " << elapsed_secs << " seconds.\n";

        if (level == 3)
            cout << "Dijkstra's took: " << elapsed_secs << " seconds.\n";

        if (level == 4)
            cout << "AStar took: " << elapsed_secs << " seconds.\n";

    } else {

        KnightBoard2 solution;

        solution.parse(input);

        cout << "Input State:\n";
        solution.print_state(0);

        clock_t begin = clock();
        
        solution.level5_computeLongestSequence();

        cout << "Final State:\n";
        solution.print_state(1);

        clock_t end = clock();
        double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;

        cout << "AStar took: " << elapsed_secs << " seconds.\n";

    }

    return 0;
}
