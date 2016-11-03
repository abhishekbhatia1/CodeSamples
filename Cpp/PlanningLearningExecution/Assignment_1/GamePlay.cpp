//*****************************************************************
//  GamePlay1.cpp
//  Planning Learning and Execution
//  Assignment 1
//
//  Created by Abhishek Bhatia.
//
//  This source file contains the GamePlay1 class method definitions.
//*****************************************************************

#include "GamePlay.h"

// typecast the input string to an integer
int GamePlay1::mystring(string str) {
    stringstream ss(str);
    long long int num;
    ss >> num;
    return num;
}

// function to parse the input file and extract relevant information
void GamePlay1::parse1(char* input) {
    freopen(input, "r", stdin);
    string str;

    getline(cin, str);
    int rep = mystring(str);

    getline(cin, str);
    num_np = mystring(str);

    for (int i = 0; i <= num_np; i++) {
        getline(cin, str);
        string first = "";
        first += str[0];
        string second = "";
        second += str[2];
        pair<int, int> loc;
        loc.first = mystring(first);
        loc.second = mystring(second);
        initial_state.push_back(loc);
    }

    getline(cin, str);
    string first = "";
    first += str[0];
    string second = "";
    second += str[2];
    goal.first = mystring(first);
    goal.second = mystring(second);
}

// action to move_left
// validates if all the preconditions are met and if the operation is valid
void GamePlay1::move_left(pair<int, int> player, vector<pair<int, int>> state, int player_idx) {
    vector<pair<int, int>> init_state = state;
    int left_coord = player.second;
    int flag = 0;
    for (int i = 0; i < state.size(); i++) {
        if (i == player_idx)
            continue;
        if (flag == 0 && state[i].first == player.first && state[i].second < left_coord) {
            left_coord = state[i].second + 1;
            flag = 1;
        } else if (flag == 1 && state[i].first == player.first) {
            left_coord = ((state[i].second >= left_coord) && (state[i].second < player.second))? state[i].second + 1 : left_coord;
        }
    }
    if (!gboard[state[player_idx].first*5 + left_coord])
        state[player_idx].second = left_coord;
    if (visited.count(from_state_to_string(state)) == 0) {
        bfs_q.push(state);
        parent[from_state_to_string(state)] = from_state_to_string(init_state);
        string act = "Move Left ";
        if (player_idx == state.size() - 1)
            act += "Player";
        else
            act += "Non Player " + to_string(player_idx + 1);
        parent_action[from_state_to_string(state)] = act;
    }
    if (DEBUG) {
    	cout << "Move " << player_idx << " left: before -> " << from_state_to_string(init_state);
    	cout << " after -> " << from_state_to_string(state) << ", " << visited.count(from_state_to_string(state)) << endl;
	}
    return;
}

// action to move_right
// validates if all the preconditions are met and if the operation is valid
void GamePlay1::move_right(pair<int, int> player, vector<pair<int, int>> state, int player_idx) {
    vector<pair<int, int>> init_state = state;
    int right_coord = player.second;
    int flag = 0;
    for (int i = 0; i < state.size(); i++) {
        if (i == player_idx)
            continue;
        if (flag == 0 && state[i].first == player.first && state[i].second > right_coord) {
            right_coord = state[i].second - 1;
            flag = 1;
        } else if (flag == 1 && state[i].first == player.first) {
            right_coord = ((state[i].second <= right_coord) && (state[i].second > player.second))? state[i].second - 1 : right_coord;
        }
    }
    if (!gboard[state[player_idx].first*5 + right_coord])
        state[player_idx].second = right_coord;
    if (visited.count(from_state_to_string(state)) == 0) {
        bfs_q.push(state);
        parent[from_state_to_string(state)] = from_state_to_string(init_state);
        string act = "Move Right ";
        if (player_idx == state.size() - 1)
            act += "Player";
        else
            act += "Non Player " + to_string(player_idx + 1);
        parent_action[from_state_to_string(state)] = act;
    }
    if (DEBUG) {
	    cout << "Move " << player_idx << " right: before -> " << from_state_to_string(init_state);
	    cout << " after -> " << from_state_to_string(state) << ", " << visited.count(from_state_to_string(state)) << endl;
	}
    return;
}

// action to move_up
// validates if all the preconditions are met and if the operation is valid
void GamePlay1::move_up(pair<int, int> player, vector<pair<int, int>> state, int player_idx) {
    vector<pair<int, int>> init_state = state;
    int up_coord = player.first;
    int flag = 0;
    for (int i = 0; i < state.size(); i++) {
        if (i == player_idx)
            continue;
        if (flag == 0 && state[i].second == player.second && state[i].first < up_coord) {
            up_coord = state[i].first + 1;
            flag = 1;
        } else if (flag == 1 && state[i].second == player.second) {
            up_coord = ((state[i].first >= up_coord) && (state[i].first < player.first))? state[i].first + 1 : up_coord;
        }
    }
    if (!gboard[state[player_idx].second + up_coord*5])
        state[player_idx].first = up_coord;
    if (visited.count(from_state_to_string(state)) == 0) {
        bfs_q.push(state);
        parent[from_state_to_string(state)] = from_state_to_string(init_state);
        string act = "Move Up ";
        if (player_idx == state.size() - 1)
            act += "Player";
        else
            act += "Non Player " + to_string(player_idx + 1);
        parent_action[from_state_to_string(state)] = act;
    }
    if (DEBUG) {
    	cout << "Move " << player_idx << " up: before -> " << from_state_to_string(init_state);
    	cout << " after -> " << from_state_to_string(state) << ", " << visited.count(from_state_to_string(state)) << endl;	
    }
    return;
}

// action to move_down
// validates if all the preconditions are met and if the operation is valid
void GamePlay1::move_down(pair<int, int> player, vector<pair<int, int>> state, int player_idx) {
    vector<pair<int, int>> init_state = state;
    int down_coord = player.first;
    int flag = 0;
    for (int i = 0; i < state.size(); i++) {
        if (i == player_idx)
            continue;
        if (flag == 0 && state[i].second == player.second && state[i].first > down_coord) {
            down_coord = state[i].first - 1;
            flag = 1;
        } else if (flag == 1 && state[i].second == player.second) {
            down_coord = ((state[i].first <= down_coord) && (state[i].first > player.first))? state[i].first - 1 : down_coord;
        }
    }
    if (!gboard[state[player_idx].second + down_coord*5])
        state[player_idx].first = down_coord;
    if (visited.count(from_state_to_string(state)) == 0) {
        bfs_q.push(state);
        parent[from_state_to_string(state)] = from_state_to_string(init_state);
        string act = "Move Down ";
        if (player_idx == state.size() - 1)
            act += "Player";
        else
            act += "Non Player " + to_string(player_idx + 1);
        parent_action[from_state_to_string(state)] = act;
    }
    if (DEBUG) {
    	cout << "Move " << player_idx << " down: before -> " << from_state_to_string(init_state);
    	cout << " after -> " << from_state_to_string(state) << ", " << visited.count(from_state_to_string(state)) << endl;
    }
    return;
}

// function to determine valid successor states to a given state
void GamePlay1::PushNeighborsInQueue(vector<pair<int, int>> state) {
    for (int i = 0; i < state.size(); i++) {
        pair<int, int> player = state[i];
        move_up(player, state, i);
        move_down(player, state, i);
        move_right(player, state, i);
        move_left(player, state, i);
    }
}

// convert state to a string for hashing purposes
string GamePlay1::from_state_to_string(vector<pair<int, int>> state) {
    string str = "";
    for (int i = 0; i < state.size(); i++) {
        str += to_string(state[i].first);
        str += to_string(state[i].second);
    }
    return str;
}

// converts a given string to a state variable
vector<pair<int, int>> GamePlay1::from_string_to_state(string str) {
    vector<pair<int, int>> state;
    for (int i = 0; i < state.size();) {
        string first = "";
        first += str[i];
        string second = "";
        second += str[i + 1];
        pair<int, int> loc;
        loc.first = mystring(first);
        loc.second = mystring(second);
        state.push_back(loc);
    }
    return state;
}

// converts a state representation to a board representation
vector<int> makeBoard(vector<pair<int, int>> state) {
	vector<int> res(25,0);
	for (int i = 0; i < state.size(); i++) {
		res[state[i].first*5 + state[i].second] = 1;
	}
	return res;
}

// Breadth First Search to search the state space and determine valid path from the start to the goal
void GamePlay1::BFS(vector<pair<int, int>> state) {
    bfs_q.push(initial_state);
    int flag = 0;
    vector<pair<int, int>> current_state;

    while(!bfs_q.empty()) {
        current_state = bfs_q.front(); bfs_q.pop();
        gboard = makeBoard(current_state);
        visited.insert(from_state_to_string(current_state));
        if (DEBUG) print_state(current_state);
        if (current_state[num_np].first == goal.first && current_state[num_np].second == goal.second) {
            cout << "Goal Found\n";
            flag = 1;
            break;
        }
        PushNeighborsInQueue(current_state);
    }
    if (flag == 0)
        cout << "Goal Not Found\n";
    if (flag) {
        string curr_str_state = from_state_to_string(current_state);
        final_path.push(curr_str_state);
        final_path_action.push(parent_action[curr_str_state]);
        while (curr_str_state != from_state_to_string(initial_state)) {
            curr_str_state = parent[curr_str_state];
            final_path.push(curr_str_state);
            if (curr_str_state != from_state_to_string(initial_state))
                final_path_action.push(parent_action[curr_str_state]);
        }
    }
    return;
}

// prints the path generated by BFS
void GamePlay1::print_path(vector<pair<int, int>> state) {
    int i = 0;
    while (!final_path.empty()) {
        string str = final_path.top();
        final_path.pop();
        cout << "State " << i << ": ";
        for (int j = 0; j < str.size() - 2;) {
            cout << "non_player " << j/2 + 1 << " (" << str[j] << "," << str[j+1] << "), ";
            j += 2;
        }
        cout << "player " << " (" << str[str.size() - 2] << "," << str[str.size() - 1] << ")" << endl;
        i++;
        if (!final_path_action.empty()) {
            cout << "Action " << i -1 << ": " << final_path_action.top() << endl;
            final_path_action.pop();
        }
    }
    return;
}

// prints a state variable
void GamePlay1::print_state(vector<pair<int, int>> state) {
	cout << "Current State: ";
	for (int i = 0; i < state.size(); i++) {
		cout << "(" << state[i].first << "," << state[i].second << ")";
		if (i == state.size() - 1)
			cout << endl;
		else
			cout << ", ";
	}
}

// function to parse input file for representation 2
void GamePlay2::parse2(char* input) {
    freopen(input, "r", stdin);
    string str;

    getline(cin, str);
    int rep = mystring(str);

    getline(cin, str);
    num_np = mystring(str);

    initial_state = new int *[5];
    for (int i = 0; i < 5; i++)
        initial_state[i] = new int[5];

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            initial_state[i][j] = 0;
        }
    }

    for (int i = 0; i <= num_np; i++) {
        getline(cin, str);
        string first = "";
        first += str[0];
        string second = "";
        second += str[2];
        if (i < num_np)
            initial_state[mystring(first)][mystring(second)] = 1;
        else
            initial_state[mystring(first)][mystring(second)] = 2;
    }

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            if (DEBUG) cout << initial_state[i][j] << " ";
        }
        if (DEBUG) cout << endl;
    }

    getline(cin, str);
    string first = "";
    first += str[0];
    string second = "";
    second += str[2];
    goal.first = mystring(first);
    goal.second = mystring(second);
}

// action to move_left
// validates if all the preconditions are met and if the operation is valid
void GamePlay2::move_left(pair<int, int> player, int** state) {
    int** init_state = state;
    init_state = new int *[5];
    for (int i = 0; i < 5; i++)
        init_state[i] = new int[5];

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            init_state[i][j] = state[i][j];
        }
    }
    int row = player.first;
    int col = player.second;
    int flag = 0;
    for (int i = 0; i < 5; i++) {
        if (i == player.second)
            continue;
        if (flag == 0 && state[row][i] > 0 && i < player.second) {
            col = i + 1;
            flag = 1;
        } else if (flag == 1 && state[row][i] > 0) {
            col = ((i >= col) && (i < player.second))? i + 1 : col;
        }
    }
    if (!init_state[row][col] && col < 5) {
        init_state[row][col] = init_state[row][player.second];
        init_state[row][player.second] = 0;
    }
    if (visited.count(from_state_to_string(init_state)) == 0) {
        bfs_q.push(init_state);
        parent[from_state_to_string(init_state)] = from_state_to_string(state);
        string act = "Move Left ";
        if (state[player.first][player.second] == 2)
            act += "Player";
        else
            act += "Non Player at (" + to_string(player.first) + ", " + to_string(player.second) + ")";
        parent_action[from_state_to_string(init_state)] = act;
    }
    if (DEBUG) {
        cout << "Move spaceship at (" << player.first << ", " << player.second << ") left: before -> " << from_state_to_string(state);
        cout << " after -> " << from_state_to_string(init_state) << ", " << visited.count(from_state_to_string(init_state)) << endl;
    }
    return;
}

// action to move_right
// validates if all the preconditions are met and if the operation is valid
void GamePlay2::move_right(pair<int, int> player, int** state) {
    int** init_state;
    init_state = new int *[5];
    for (int i = 0; i < 5; i++)
        init_state[i] = new int[5];

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            init_state[i][j] = state[i][j];
        }
    }
    int row = player.first;
    int col = player.second;
    int flag = 0;
    for (int i = 0; i < 5; i++) {
        if (i == player.second)
            continue;
        if (flag == 0 && state[row][i] > 0 && i > player.second) {
            col = i - 1;
            flag = 1;
        } else if (flag == 1 && state[row][i] > 0) {
            col = ((i <= col) && (i > player.second))? i - 1 : col;
        }
    }
    if (!init_state[row][col] && col >= 0) {
        init_state[row][col] = init_state[row][player.second];
        init_state[row][player.second] = 0;
    }
    if (visited.count(from_state_to_string(init_state)) == 0) {
        bfs_q.push(init_state);
        parent[from_state_to_string(init_state)] = from_state_to_string(state);
        string act = "Move Right ";
        if (state[player.first][player.second] == 2)
            act += "Player";
        else
            act += "Non Player at (" + to_string(player.first) + ", " + to_string(player.second) + ")";
        parent_action[from_state_to_string(init_state)] = act;
    }
    if (DEBUG) {
        cout << "Move spaceship at (" << player.first << ", " << player.second << ") right: before -> " << from_state_to_string(state);
        cout << " after -> " << from_state_to_string(init_state) << ", " << visited.count(from_state_to_string(init_state)) << endl;
    }
    return;
}

// action to move_up
// validates if all the preconditions are met and if the operation is valid
void GamePlay2::move_up(pair<int, int> player, int** state) {
    int** init_state;
    init_state = new int *[5];
    for (int i = 0; i < 5; i++)
        init_state[i] = new int[5];
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            init_state[i][j] = state[i][j];
        }
    }
    int row = player.first;
    int col = player.second;
    int flag = 0;
    for (int i = 0; i < 5; i++) {
        if (i == player.first)
            continue;
        if (flag == 0 && state[i][col] > 0 && i < player.first) {
            row = i + 1;
            flag = 1;
        } else if (flag == 1 && state[i][col] > 0) {
            row = ((i >= row) && (i < player.first))? i + 1 : row;
        }
    }
    if (!init_state[row][col] && row < 5) {
        init_state[row][col] = init_state[player.first][col];
        init_state[player.first][col] = 0;
    }
    if (visited.count(from_state_to_string(init_state)) == 0) {
        bfs_q.push(init_state);
        parent[from_state_to_string(init_state)] = from_state_to_string(state);
        string act = "Move Up ";
        if (state[player.first][player.second] == 2)
            act += "Player";
        else
            act += "Non Player at (" + to_string(player.first) + ", " + to_string(player.second) + ")";
        parent_action[from_state_to_string(init_state)] = act;
    }
    if (DEBUG) {
        cout << "Move spaceship at (" << player.first << ", " << player.second << ") up: before -> " << from_state_to_string(state);
        cout << " after -> " << from_state_to_string(init_state) << ", " << visited.count(from_state_to_string(init_state)) << endl;
    }
    return;
}

// action to move_down
// validates if all the preconditions are met and if the operation is valid
void GamePlay2::move_down(pair<int, int> player, int** state) {
    int** init_state;
    init_state = new int *[5];
    for (int i = 0; i < 5; i++)
        init_state[i] = new int[5];

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            init_state[i][j] = state[i][j];
        }
    }
    int row = player.first;
    int col = player.second;
    int flag = 0;
    for (int i = 0; i < 5; i++) {
        if (i == player.first)
            continue;
        if (flag == 0 && state[i][col] > 0 && i > player.first) {
            row = i - 1;
            flag = 1;
        } else if (flag == 1 && state[i][col] > 0) {
            row = ((i <= row) && (i > player.first))? i - 1 : row;
        }
    }
    if (!init_state[row][col] && row >= 0) {
        init_state[row][col] = init_state[player.first][col];
        init_state[player.first][col] = 0;
    }
    if (visited.count(from_state_to_string(init_state)) == 0) {
        bfs_q.push(init_state);
        parent[from_state_to_string(init_state)] = from_state_to_string(state);
        string act = "Move Down ";
        if (state[player.first][player.second] == 2)
            act += "Player";
        else
            act += "Non Player at (" + to_string(player.first) + ", " + to_string(player.second) + ")";
        parent_action[from_state_to_string(init_state)] = act;
    }
    if (DEBUG) {
        cout << "Move spaceship at (" << player.first << ", " << player.second << ") down: before -> " << from_state_to_string(state);
        cout << " after -> " << from_state_to_string(init_state) << ", " << visited.count(from_state_to_string(init_state)) << endl;
    }
    return;
}

// generates successor states to the current state
void GamePlay2::PushNeighborsInQueue(int** state) {
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            if (state[i][j] > 0) {
                pair<int, int> player;
                player.first = i;
                player.second = j;
                move_up(player, state);
                move_down(player, state);
                move_right(player, state);
                move_left(player, state);
            }
        }
    }
}

// converts the state variable to a string for hashing purposes
string GamePlay2::from_state_to_string(int** state) {
    string str = "";
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            if (state[i][j]) {
                str += to_string(i);
                str += to_string(j);
                str += to_string(state[i][j]);
            }
        }
    }
    return str;
}

// converts a string to a state variable
int** GamePlay2::from_string_to_state(string str) {
    int** state;
    state = new int *[5];
    for (int i = 0; i < 5; i++)
        state[i] = new int[5];

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            state[i][j] = 0;
        }
    }

    for (int i = 0; i < str.size();) {
        string first = "";
        first += str[i];
        string second = "";
        second += str[i + 1];
        string third = "";
        third += str[i + 2];
        state[mystring(first)][mystring(second)] = mystring(third);
        i = i+3;
    }
    return state;
}

// BFS to search the state space and determine valid path between the start and the goal
void GamePlay2::BFS(int** state) {
    bfs_q.push(initial_state);
    int flag = 0;
    int** current_state;

    while(!bfs_q.empty()) {
        current_state = bfs_q.front(); bfs_q.pop();
        visited.insert(from_state_to_string(current_state));
        if (DEBUG) print_state(current_state);
        if (current_state[goal.first][goal.second] == 2) {
            cout << "Goal Found\n";
            flag = 1;
            break;
        }
        PushNeighborsInQueue(current_state);
    }
    if (flag == 0)
        cout << "Goal Not Found\n";
    if (flag) {
        string curr_str_state = from_state_to_string(current_state);
        final_path.push(curr_str_state);
        final_path_action.push(parent_action[curr_str_state]);
        while (curr_str_state != from_state_to_string(initial_state)) {
            curr_str_state = parent[curr_str_state];
            final_path.push(curr_str_state);
            if (curr_str_state != from_state_to_string(initial_state))
                final_path_action.push(parent_action[curr_str_state]);
        }
    }
    return;
}

// prints the path generated by BFS
void GamePlay2::print_path(int** state) {
    int i = 0;
    while (!final_path.empty()) {
        string str = final_path.top();
        final_path.pop();
        cout << "State " << i << ": \n";
        int** print_state;
        print_state = new int *[5];
        for (int i = 0; i < 5; i++)
            print_state[i] = new int[5];

        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                print_state[i][j] = 0;
            }
        }
        print_state = from_string_to_state(str);
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                cout << print_state[i][j] << " ";
            }
            cout << endl;
        }
        i++;
        if (!final_path_action.empty()) {
            cout << "Action " << i -1 << ": " << final_path_action.top() << endl;
            final_path_action.pop();
        }
    }
    return;
}

// prints each state variable for representation 2
void GamePlay2::print_state(int** state) {
    cout << "Current State: \n";
    int flag = 0;
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            cout << state[i][j] << " ";
        }
        cout << endl;
    }
}

//*****************************************************************
// End of File
//*****************************************************************