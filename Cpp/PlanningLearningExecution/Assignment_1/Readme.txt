Readme.txt:
1) This file describes the folder contents of the code directory for Homework 1, Planning, Execution, and Learning 15-887.

Directory Structure:
1) The GamePlay.h header file contains the GamePlay class declaration. 
2) The GamePlay.cpp file contains the method definitions of the GamePlay class.
3) main.cpp source file that parses the input file, utilizes the GamePlay class and generates the output

Important Files:
1) problem_file_b_p9.txt, problem_file_i_p18.txt, problem_file_a_p27.txt, and problem_file_e_p36.txt are the input files
2) main is the executable generated that reads the input, executes the code and dumps the output to standard output

Compiling and Executing the code:
1) Compile: g++ -std=c++11 main.cpp -o main
2) Execute: ./main Representation_Number(1/2) Input_Problem_File
3) Sample Complie and Execute command line: g++ -std=c++11 main.cpp -o main ; ./main 1 problem_file_b_p9.txt

Input File:
1) Line 1 -> representation (0/1), however this variable is redundant now and gets overwritten by the represenation number passed from the commandline.
2) Line 2 -> number of non players.
3) Next n (number of non players) lines -> initial coordinates of each non player.
4) Next Line -> initial coordinates of the player.
5) Next Line -> goal location.