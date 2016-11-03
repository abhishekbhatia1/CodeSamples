Readme.txt:
1) This file describes the folder contents of the code directory for Homework 2, Planning, Execution, and Learning 15-887.

Directory Structure:
1) The MovingTarget.h header file contains the MovingTarget class declaration. 
2) The MovingTarget.cpp file contains the method definitions of the MovingTarget class.
3) main.cpp source file that parses the input file, utilizes the MovingTarget class and generates the output

Important Files:
1) problem_file_b_p9.txt, problem_file_i_p18.txt, problem_file_a_p27.txt, and problem_file_e_p36.txt are the input files
2) main is the executable generated that reads the input, executes the code and dumps the output to standard output

Compiling and Executing the code:
1) Compile: g++ -std=c++11 main.cpp -o main
2) Execute: ./main planner#(1/2) ProblemFile
NOTE: 
Planner 1: Non Optimal, but computationally faster
Planner 2: Planner: Computationally slower, but optimal
3) Sample Complie and Execute command line: g++ -std=c++11 main.cpp -o main ; ./main 1 problem_0.txt > out.txt
