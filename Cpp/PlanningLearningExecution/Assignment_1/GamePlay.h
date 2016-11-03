//*****************************************************************
//  GamePlay1.h
//  Planning Learning and Execution
//  Assignment 1
//
//  Created by Abhishek Bhatia.
//
//  This header file contains the GamePlay1 class declaration.
//*****************************************************************

#include <bits/stdc++.h>
using namespace std;

#define DEBUG 0

//*****************************************************************
// GamePlay1 Class
//*****************************************************************
class GamePlay1
{
private:
    
public:
    int num_np; // number of non players
    vector<pair<int, int>> initial_state; // initial state representation 1
    queue<vector<pair<int, int>>> bfs_q; // queue to store valid states during the bfs search
    unordered_set<string> visited; // set to store visited states
    unordered_map<string, string> parent; // mapping from a state to a parent state
    unordered_map<string, string> parent_action; // mapping from an action to a parent action
    stack<string> final_path; // stack to store the final path
    stack<string> final_path_action; // stack to store the final actions taken to get to the final path
    pair<int, int> goal; // goal location
    vector<int> gboard; // game board represented as a vector
    
    int mystring(string str);
    void parse1(char* input);
    void move_up(pair<int, int> player, vector<pair<int, int>> state, int player_idx);
    void move_down(pair<int, int> player, vector<pair<int, int>> state, int player_idx);
    void move_left(pair<int, int> player, vector<pair<int, int>> state, int player_idx);
    void move_right(pair<int, int> player, vector<pair<int, int>> state, int player_idx);
    void PushNeighborsInQueue(vector<pair<int, int>> state);
    string from_state_to_string(vector<pair<int, int>> state);
    vector<pair<int, int>> from_string_to_state(string str);
    void BFS(vector<pair<int, int>> state);
    void print_path(vector<pair<int, int>> state);
    void print_state(vector<pair<int, int>> state);
};

class GamePlay2 : public GamePlay1
{
private:

public:
    int** initial_state; // initial state representation 2
    queue<int**> bfs_q; // queue to store valid states during the bfs 

    void parse2(char* input);
    void move_up(pair<int, int> player, int** state);
    void move_down(pair<int, int> player, int** state);
    void move_left(pair<int, int> player, int** state);
    void move_right(pair<int, int> player, int** state);
    void PushNeighborsInQueue(int** state);
    string from_state_to_string(int** state);
    int** from_string_to_state(string str);
    void BFS(int** state);
    void print_path(int** state);
    void print_state(int** state);
};

//*****************************************************************
// End of File
//*****************************************************************