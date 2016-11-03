//*****************************************************************
//  TCC.cpp
//
//  Created by Abhishek Bhatia.
//
//  This header file contains the TCC class declaration.
//*****************************************************************

#include "TCC.h"

// function to parse the input string and extract relevant information
void TCC::parse(string str) {
    long long int i;
    string left = "";

    //extract the left hand side
    for (i = 0;i < str.size(); i++)
    { 
        if(str[i] == '=') break;
        if(str[i] == ' ') continue;
        left += str[i];
    }

    //store mapping of the variable
    if (mp.count(left) == 0)
        mp[left] = count++;
    
    ++i;

    while (i < str.size())
    {
        string temp = "";
        while (i < str.size() && str[i] != '+')
        {
            if (str[i] != ' ')
                temp += str[i];
            ++i;
        }

        //check is integer or variable
        if (temp[0] >= '0' && temp[0] <= '9')
        {
            long long int num = mystring(temp);
            v[mp[left]].push_back(num);
            c[mp[left]].push_back(1);
        } else
        {
            if (mp.count(temp) == 1)
                v[mp[left]].push_back(mp[temp]);
            else
            {
                mp[temp] = count++;
                v[mp[left]].push_back(mp[temp]);
            }
            c[mp[left]].push_back(0);
        }
        ++i;
    }
}

//recursive function for traversing the tree in a dfs manner
long long int TCC::rec(long long int node)
{
    long long int i, ans = 0;
    if (values.count(node) == 1)
        return values[node];
    for (i = 0;i < v[node].size(); i++)
    {
        if (c[node][i] == 0)
        {
            //go to child node as it is a variable
            ans += rec(v[node][i]);
        }else
        {
            //as it is an integer so simply add the value
            ans += v[node][i];
        }
    }
    values[node] = ans;
    return ans;
}

//typecast the input string to an integer
long long int TCC::mystring(string str)
{
    stringstream ss(str);
    long long int num;
    ss >> num;
    return num;
}

//*****************************************************************
// End of File
//*****************************************************************