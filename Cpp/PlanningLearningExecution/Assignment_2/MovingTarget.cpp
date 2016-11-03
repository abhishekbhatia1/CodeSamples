//*****************************************************************
//  MovingTarget1.cpp
//  Planning Learning and Execution
//  Assignment 2
//
//  Created by Abhishek Bhatia.
//
//  This source file contains the MovingTarget1 class method definitions.
//*****************************************************************

#include "MovingTarget.h"

int MovingTarget1::myint(string str) {
    stringstream ss(str);
    long long int num;
    ss >> num;
    return num;
}

pair<int, int> MovingTarget1::pair_from_string(string str) {
    string s1 = "", s2 = "";
    int i;
    for (i = 0; i < str.size(); i++) { 
        if(str[i] == ',') break;
        s1 += str[i];
    }
    i = i + 1;
    while (i < str.size()) {
        s2 += str[i];
        i++;
    }
    pair<int, int> loc;
    loc.first = myint(s1);
    loc.second = myint(s2);
    return loc;
}

vector<int> MovingTarget1::vector_from_string(string str) {
    string s1 = "";
    vector<int> res;
    for (int i = 0; i < str.size(); i++) { 
        if(str[i] == ',') {
            res.push_back(myint(s1));
            s1 = "";
        } else {
            s1 += str[i];
        }
    }
    res.push_back(myint(s1));
    return res;
}

void MovingTarget1::parse(char* input) {
    freopen(input, "r", stdin);
    string str;

    getline(cin, str);
    int flag = 0;
    while (1) {
        switch (str[0]) {
            case 'N':
                getline(cin, str);
                n = myint(str);
                getline(cin, str);
                break;
            case 'R':
                getline(cin, str);
                r_init = pair_from_string(str);
                getline(cin, str);
                break;
            case 'T':
                getline(cin, str);
                while(str[0] != 'B') {
                    tar_pos.push_back(pair_from_string(str));
                    getline(cin, str);
                }
                break;
            case 'B':
                while(getline(cin, str)) {
                    cost.push_back(vector_from_string(str));
                }
                flag = 1;
                break;
        }
        if (flag)
            break;
    }
    fclose(stdin);
}

int MovingTarget1::heu(pair<int, int> current, pair<int, int> ms) {
    return abs(current.first - ms.first) + abs(current.second - ms.second);
}

int MovingTarget1::GenerateSuccesors(pair<int, int> loc) {
    int del_x, del_y;
    for (int i = 0; i < 5; i++) {
        switch (i) {
            case 0:
                del_x = 1;
                del_y = 0;
                break;
            case 1:
                del_x = -1;
                del_y = 0;
                break;
            case 2:
                del_x = 0;
                del_y = 1;
                break;
            case 3:
                del_x = 0;
                del_y = -1;
                break;
            case 4:
                del_x = 0;
                del_y = 0;
                break;
        }
        pair<int, int> new_loc;
        new_loc.first = loc.first + del_x;
        new_loc.second = loc.second + del_y;
        int fl = 0;
        if ((new_loc.first >= 0 && new_loc.first < n) && (new_loc.second >= 0 && new_loc.second < n)) {
            if (visited.count(new_loc) == 0) {
                fl = 1;
                pair<pair<int, int>, int> node;
                node.first = new_loc;
                node.second = g_val[loc] + cost[new_loc.first][new_loc.second] + 1*heu(new_loc, goal);
                if (g_val.count(new_loc) == 0) {
                    q_astar.push(node);
                    parent[new_loc] = loc;
                    g_val[new_loc] = g_val[loc] + cost[new_loc.first][new_loc.second];
                    gf_val[new_loc] = gf_val[loc] + 1;
                } else {
                    if (node.second < g_val[new_loc]) {
                        q_astar.push(node);
                        parent[new_loc] = loc;
                        g_val[new_loc] = g_val[loc] + cost[new_loc.first][new_loc.second];
                        gf_val[new_loc] = gf_val[loc] + 1;
                    }
                }
            }
            if (new_loc == goal) {
                return 1;
            }
        }
    }
    return 0;
}

void MovingTarget1::wAstar() {
    pair<pair<int, int>, int> node;
    node.first = r_init;
    node.second = cost[r_init.first][r_init.second] + heu(r_init, goal);
    g_val[r_init] = cost[r_init.first][r_init.second];
    gf_val[r_init] = 1;
    q_astar.push(node);
    int flag = 0;
    int idx;

    while(!q_astar.empty()) {
        node = q_astar.top(); q_astar.pop();
        nodes_expanded++;
        current = node.first;
        idx = gf_val[current];
        goal = tar_pos[idx];
        if (DEBUG) cout << "Current: " << current.first << ", " << current.second << endl;
        if (DEBUG) cout << "F: " << node.second << endl;
        if (DEBUG) cout << "Goal: " << goal.first << ", " << goal.second << endl;
        if (DEBUG) cout << "Idx: " << idx << endl;
        visited.insert(current);
        if (GenerateSuccesors(current)) {
            cout << "Goal Found\n";
            flag = 1;
            break;
        }
    }
    if (flag == 0)
        cout << "Goal Not Found\n";
    if (flag) {
        node.first = goal;
        node.second = gf_val[current];
        final_path.push(node);
        node.first = current;
        node.second = gf_val[current];
        final_path.push(node);
        while (current != r_init) {
            current = parent[current];
            node.first = current;
            node.second = gf_val[current];
            if (current != r_init)
                final_path.push(node);
        }
        node.first = r_init;
        node.second = gf_val[current];
        final_path.push(node);
    }
        
    while(!final_path.empty()) {
        pair<pair<int, int>, int> loc = final_path.top();
        final_path.pop();
        if (final_path.empty()) {
            cout << "Robot location: (" << loc.first.first << ", " << loc.first.second << ") and Target location: (" << tar_pos[loc.second].first << ", " << tar_pos[loc.second].second << ")\n"; 
        }
        else { 
            cout << "Robot location: (" << loc.first.first << ", " << loc.first.second << ") and Target location: (" << tar_pos[loc.second-1].first << ", " << tar_pos[loc.second-1].second << ")\n"; 
            cost_path += cost[loc.first.first][loc.first.second];
        }
    }return;
}

void MovingTarget2::GenerateSuccesorsF(pair<int, int> loc) {
    int del_x, del_y;
    for (int i = 0; i < 4; i++) {
        switch (i) {
            case 0:
                del_x = 1;
                del_y = 0;
                break;
            case 1:
                del_x = -1;
                del_y = 0;
                break;
            case 2:
                del_x = 0;
                del_y = 1;
                break;
            case 3:
                del_x = 0;
                del_y = -1;
                break;
        }
        pair<int, int> new_loc;
        new_loc.first = loc.first + del_x;
        new_loc.second = loc.second + del_y;
        if ((new_loc.first >= 0 && new_loc.first < n) && (new_loc.second >= 0 && new_loc.second < n)) {
            if (visited.count(new_loc) == 0) {
                pair<pair<int, int>, int> node;
                node.first = new_loc;
                node.second = g_val[loc] + cost[new_loc.first][new_loc.second];
                if (g_val.count(new_loc) == 0) {
                    q_astar.push(node);
                    parent[new_loc] = loc;
                    g_val[new_loc] = g_val[loc] + cost[new_loc.first][new_loc.second];
                } else {
                    if (node.second < g_val[new_loc]) {
                        q_astar.push(node);
                        parent[new_loc] = loc;
                        g_val[new_loc] = g_val[loc] + cost[new_loc.first][new_loc.second];
                    }
                }
            }
        }
    }
    return;
}

void MovingTarget2::Dijkstras() {
    pair<pair<int, int>, int> node;
    node.first = r_init;
    node.second = 0;
    g_val[r_init] = 0;
    q_astar.push(node);
    int idx;

    while(!q_astar.empty()) {
        node = q_astar.top(); q_astar.pop();
        nodes_expanded ++;
        current = node.first;
        idx = gf_val[current];
        goal = tar_pos[idx];
        if (DEBUG) cout << "Current: " << current.first << ", " << current.second << endl;
        if (DEBUG) cout << "F: " << node.second << endl;
        if (DEBUG) cout << "Goal: " << goal.first << ", " << goal.second << endl;
        if (DEBUG) cout << "Idx: " << idx << endl;
        if (visited.count(current) == 0) {
            visited.insert(current);
            GenerateSuccesorsF(current);
        }
    }
    return;
}

void MovingTarget2::GenerateSuccesorsB(pair<pair<int, int>, pair<int, int>> node_in) {
    int del_x, del_y;
    pair<int, int> loc = node_in.first;
    pair<int, int> loc_c = node_in.second;
    for (int i = 0; i < 5; i++) {
        switch (i) {
            case 0:
                del_x = 0;
                del_y = -1;
                break;
            case 1:
                del_x = 1;
                del_y = 0;
                break;
            case 2:
                del_x = 0;
                del_y = 1;
                break;
            case 3:
                del_x = -1;
                del_y = 0;
                break;
            case 4:
                del_x = 0;
                del_y = 0;
                break;
        }
        pair<int, int> new_loc;
        new_loc.first = loc.first + del_x;
        new_loc.second = loc.second + del_y;

        if ((new_loc.first >= 0 && new_loc.first < n) && (new_loc.second >= 0 && new_loc.second < n)) {
            pair<pair<int, int>, pair<int, int>> node;
            node.first = new_loc;
            node.second.first = node_in.second.first + cost[new_loc.first][new_loc.second] + g_val[new_loc] - g_val[loc];
            node.second.second = node_in.second.second - 1;
            pair<pair<int, int>, int> nod;
            nod.first = node.first;
            nod.second = node.second.second;
            if (visited2.count(nod) == 0) {
                if (node.second.second >= 0) {
                    q_astar2.push(node);
                    pair<pair<int, int>, int> par1, par2;
                    par1.first = node_in.first;
                    par1.second = node_in.second.second;
                    par2.first = node.first;
                    par2.second = node.second.second;
                    parent2[par2] = par1;
                    if (DEBUG) cout << "Succ: " << node.first.first << "," << node.first.second << "," << node.second.second 
                    << ", G: " << node_in.second.first + cost[new_loc.first][new_loc.second] - g_val[loc] << ", H: " << g_val[new_loc] << endl;
                }
            }
        }
    }
    return;
}

void MovingTarget2::BAstar() {
    pair<pair<int, int>, int> dummy, par;
    dummy.first.first = 1001;
    dummy.first.second = 1001;
    dummy.second = 1001;
    pair<pair<int, int>, pair<int, int>> node;
    for (int i = 1; i < tar_pos.size(); i++) {
        node.first = tar_pos[i];
        node.second.first = cost[tar_pos[i].first][tar_pos[i].second] + g_val[tar_pos[i]];
        node.second.second = i;
        if (i > heu(node.first, r_init))   
            q_astar2.push(node);
        par.first = node.first;
        par.second = i;
        parent2[par] = dummy; 
    }
    int flag = 0;

    while(!q_astar2.empty()) {
        node = q_astar2.top(); q_astar2.pop();
        nodes_expanded++;
        current = node.first;
        goal = r_init;
        if (DEBUG) cout << "Current: " << current.first << "," << current.second << "," << node.second.second << ", F: " << node.second.first << endl;
        pair<pair<int, int>, int> nod;
        nod.first = node.first;
        nod.second = node.second.second;
        if (current == goal && node.second.second == 0) {
            cout << "Goal Found\n";
            flag = 1;
            break;
        } else {
            if (visited2.count(nod) == 0)
                GenerateSuccesorsB(node);
        }
        visited2.insert(nod);
    }
    if (flag == 0)
        cout << "Goal Not Found\n";
    if (flag) {
        pair<pair<int, int>, int> nodeg, nodec;
        nodeg.first = goal;
        nodeg.second = g_val[node.first];
        nodec.first = current;
        nodec.second = node.second.second;
        final_path.push(nodeg);
        while (nodec != dummy) {
            nodec = parent2[nodec];
            if (nodec != dummy)
                final_path.push(nodec);
        }
    }
    
    int final_cost = 0;
    int idx = 0;
    while(!final_path.empty()) {
        pair<pair<int, int>, int> loc = final_path.front();
        final_path.pop();
        cout << "Robot location: (" << loc.first.first << ", " << loc.first.second << ") and "
             << "Target location: (" << tar_pos[idx].first << ", " << tar_pos[idx].second << ")\n";
        idx++;
        if (!final_path.empty())
            cost_path += cost[loc.first.first][loc.first.second];
    }
    return;
}

//*****************************************************************
// End of File
//*****************************************************************
