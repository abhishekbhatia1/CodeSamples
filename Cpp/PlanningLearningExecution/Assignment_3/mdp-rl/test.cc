#include "mdp-simulation.h"
#include <iostream>
#include <bits/stdc++.h>

using namespace std;

double Q[MAX_GRID*MAX_GRID][4] = {0};

double alpha = 0.01;

double discount = 0.9;

int num_episodes = 1000000;

int itr_episode = 100;

int eps = 95;

double reward_vec[1000000] = {0};

Action idx_to_action(int idx) {
	switch(idx) {
		case 0:
			return N;
			break;
		case 1:
			return S;
			break;
		case 2:
			return E;
			break;
		case 3:
			return W;
			break;
	};
}

char idx_to_actionchar(int idx) {
	switch(idx) {
		case 0:
			return 'N';
			break;
		case 1:
			return 'S';
			break;
		case 2:
			return 'E';
			break;
		case 3:
			return 'W';
			break;
	};
}

int main (void)
{
	for (int i = 0; i < num_episodes; i++) {
		// select a state randomly
		int state_r = rand()%10;
		int state_c = rand()%10;
		int curr_st = state_r * 10 + state_c;
		for (int j = 0; j < itr_episode; j++) {
			// store the reward for each episode
			reward_vec[i] += my_reward(State(state_r, state_c));
			
			// select an action using the epsilon greedy approach
			int curr_ac;
			int rand_eps = rand()%100;
			int max_q = INT_MIN;
			if (rand_eps < eps) {
				for (int idx = 0; idx < 4; idx++) {
					if (Q[curr_st][idx] > max_q) {
						max_q = Q[curr_st][idx];
						curr_ac = idx;
					}
				}
			} else {
				curr_ac = rand()%4;
			}

			// determine next state from current state and current action
			State nextState = my_next_state(State(state_r, state_c), idx_to_action(curr_ac));
			int state_r_next = nextState.x;
			int state_c_next = nextState.y;
			int nex_st = state_r_next * 10 + state_c_next;

			// determine next action using the greedy approach
			int nex_ac;
			max_q = INT_MIN;
			for (int idx = 0; idx < 4; idx++) {
				if (Q[nex_st][idx] > max_q) {
					max_q = Q[nex_st][idx];
					nex_ac = idx;
				}
			}

			// update the Q value for current state and current action
			Q[curr_st][curr_ac] = (1 - alpha) * Q[curr_st][curr_ac] + alpha * (my_reward(State(state_r, state_c)) + discount * Q[nex_st][nex_ac]);

			// update current state for next iteration
			curr_st = nex_st;
			state_r = state_r_next;
			state_c = state_c_next;
		}
		cout << reward_vec[i] << endl;
	}
  	
  	// print learnt Q values
  	int final_policy[MAX_GRID*MAX_GRID] = {0};
	for (int i = 0; i < MAX_GRID; i++) {
		for (int j = 0; j < MAX_GRID; j++) {
			int m_idx = 0;
			int m_val = INT_MIN;
			for (int k = 0; k < 4; k++) {
				//cout << Q[i*10+j][k] << " ";
				if (Q[i*10+j][k] > m_val) {
					m_idx = k;
					m_val = Q[i*10+j][k];
				}
			}
			//cout << endl;
			final_policy[i*10+j] = m_idx;
		}
	}

	//cout << " \n";

	// print readable representation of the final policy
	for (int i = 0; i < MAX_GRID; i++) {
		for (int j = 0; j < MAX_GRID; j++) {
			//cout << idx_to_actionchar(final_policy[i*10+j]) << " ";
			//cout << idx_to_actionchar(final_policy[i+j*10]) << " ";
		}
		//cout << endl;
	}
	
	/*State nextState = my_next_state(State(0, 0), N);
	cout << "From 0, 0 to " << nextState.x << ", " << nextState.y << endl;
	Reward reward = my_reward(State(1, 1));
	cout << "Receiving reward " << reward << endl;*/
	
	return 0;
}
