#include <iostream>
#include <vector>
#include <Eigen/Dense>
#include <queue>
#include <stack>

// This header contains documentation for the interface you should implement as well as useful
// constants which are relevant to the simulation.  Click the Help link at the top of the
// page to see a link to the contents of this header.
#include "sim.h"

// Any state you wish to maintain can be placed here and stored as global variables.
#define GridScale 3 //Macro 
int grid[int(MAX_X)*GridScale][int(MAX_Y)*GridScale] = {0}; //2-D Array to define the configuration space including the boundaries and obstacles
int visited[int(MAX_X)*GridScale][int(MAX_Y)*GridScale] = {0}; //2-D Array to track visited neighbors for BFS
int parent_x[int(MAX_X)*GridScale][int(MAX_Y)*GridScale] = {0}; //2-D Array to track the x coordinate of the parent of every vertex for BFS
int parent_y[int(MAX_X)*GridScale][int(MAX_Y)*GridScale] = {0}; //2-D Array to track the y coordinate of the parent of every vertex for BFS
std::stack<float> final_path_x; //stack to store the x coordinates of the final path 
std::stack<float> final_path_y; //stack to store the y coordinates of the final path
std::queue<float> q_x; //queue used in BFS, stores x coordinates 
std::queue<float> q_y; //queue used in BFS, stores y coordinates
Eigen::Vector2d Goal_Pos; //Global Variable used to store the Goal Position
Eigen::Vector2d next_position; //Global Variable used to store the Next Position
int bfs_flag = 0;


// [Obsolete] This method is used to determine collision free next valid position from given current position. This method is no longer used in ComputeControl.
Eigen::Vector2d NextPosition(const Eigen::Vector2d& vehicle_position) {
	Eigen::Vector2d next_position;
	int x = vehicle_position.x();
	int y = vehicle_position.y();
	Eigen::Vector2d point = vehicle_position;
	float min = INT_MAX;
	for (int i = 0; i < 5; i++) {
		switch (i) {
			case 0 :
				if (x - 1 >= MIN_X && grid[x - 1][y] != 1) {
					point.x() = x - 1;
					point.y() = y;					
				}
				break;
			case 1 :
				if (x - 1 >= MIN_X && y + 1 < MAX_Y && grid[x - 1][y + 1] != 1) {
					point.x() = x - 1;
					point.y() = y + 1;
				}
				break;
			case 2 :
				if (y + 1 < MAX_Y && grid[x][y + 1] != 1) {
					point.x() = x;
					point.y() = y + 1;
				}
				break;
			case 3 :
				if (x + 1 < MAX_X && y + 1 < MAX_Y && grid[x + 1][y + 1] != 1) {
					point.x() = x + 1;
					point.y() = y + 1;
				}
				break;
			case 4 :
				if (x + 1 < MAX_X && grid[x + 1][y] != 1) {
					point.x() = x + 1;
					point.y() = y;
				}
				break;
		}
		float distance = sqrt(pow(Goal_Pos.x() - point.x(), 2) + pow(Goal_Pos.y() - point.y(), 2));
		if (distance < min) {
			min = distance;
			next_position.x() = point.x();
			next_position.y() = point.y();
		}
	}
	return next_position;
}

// This method is used to push valid (not visited and collision free) neighbors into the BFS queue. Once pushed into the queue, these vertices are marked visited
// and the parent arrays are updated accordingly.
void PushNeighborsInQueue(const Eigen::Vector2d& vehicle_position) {
	int start_x = vehicle_position.x() - 1 >= MIN_X ? vehicle_position.x() - 1 : MIN_X;
  	int end_x = vehicle_position.x() + 1 < MAX_X*GridScale ? vehicle_position.x() + 1 : MAX_X*GridScale;
  	int start_y = vehicle_position.y() - 1 >= MIN_Y ? vehicle_position.y() - 1 : MIN_Y;
  	int end_y = vehicle_position.y() + 1 < MAX_Y*GridScale ? vehicle_position.y() + 1 : MAX_Y*GridScale;
  	for (int i = start_x; i <= end_x; i++) {
  		for (int j = start_y; j <= end_y; j++) {
  			if (i == vehicle_position.x() && j == vehicle_position.y())
  				continue;
  			else {
  				if (!visited[i][j]) {
  					if (!grid[i][j]) {
  						q_x.push(i);
  						q_y.push(j);	
  						visited[i][j] = 1;
  						parent_x[i][j] = vehicle_position.x();
  						parent_y[i][j] = vehicle_position.y();
  					}
  				}
  			}
  		}
  	}
}

// Breadth First Search, the algorithm used to traverse the graph to determine a valid collision-free path between the vehicle_position and goal_position.
// The algorithm starts with the vehicle_position and explores all the neighbors till either a goal_position is found or all the vertices are visited.
// If a valid path is determined between the vehicle_position and goal_position, the bfs_flag is set as true (which will be used in ComputeControl) and the path
// is stored in a stack.
void BFS(const Eigen::Vector2d& vehicle_position, const Eigen::Vector2d& goal_position) {
	q_x.push(vehicle_position.x());
	q_y.push(vehicle_position.y());
	visited[int(vehicle_position.x())][int(vehicle_position.y())] = 1;
	Eigen::Vector2d current_position;
	while (!q_x.empty()) {
		current_position.x() = q_x.front() ; q_x.pop();
		current_position.y() = q_y.front() ; q_y.pop();
		int cp_x = current_position.x();
		int cp_y = current_position.y();
		int gp_x = goal_position.x();
		int gp_y = goal_position.y();
		if (current_position.x() == int(goal_position.x()) && current_position.y() == int(goal_position.y())) {
			break;
		}
		PushNeighborsInQueue(current_position);
	}
	if (current_position.x() == int(goal_position.x()) && current_position.y() == int(goal_position.y())) {
		bfs_flag = 1;
		while(current_position.x() != int(vehicle_position.x()) || current_position.y() != int(vehicle_position.y())) {
			int cur_pos_x = current_position.x(), cur_pos_y = current_position.y();
			final_path_x.push(current_position.x());
			final_path_y.push(current_position.y());
			current_position.x() = parent_x[cur_pos_x][cur_pos_y];
			current_position.y() = parent_y[cur_pos_x][cur_pos_y];
		}	
	} else {
		std::cout << "Breadth First Search couldn't find a collision free path between the vehicle_position and goal_position\n";
	}
}

// This method is called once when the simulation starts.
// The first thing initialized is the grid by updating vertices alond the boundaries and vertices in collision with the object.
// Then the BFS method is called to determine a collision-free path between the vehicle_position and the goal_position
void Initialize(const Eigen::Vector2d& vehicle_position, const Eigen::Vector2d& goal_position,
                const std::vector<Eigen::Vector2d>& obstacles) {
  //Set global variable Goal_Pos
  Goal_Pos.x() = goal_position.x();
  Goal_Pos.y() = goal_position.y();

  //Update the grid considering the obstacles
  for (int i = 0; i < obstacles.size(); i++) {
  	int start_x = (obstacles[i].x() - OBSTACLE_RADIUS - VEHICLE_RADIUS)*GridScale + 1;
  	int end_x = (obstacles[i].x() + OBSTACLE_RADIUS + VEHICLE_RADIUS)*GridScale;
  	int start_y = (obstacles[i].y() - OBSTACLE_RADIUS - VEHICLE_RADIUS)*GridScale + 1;
  	int end_y = (obstacles[i].y() + OBSTACLE_RADIUS + VEHICLE_RADIUS)*GridScale;
  	if (start_x < MIN_X) {
  		start_x = MIN_X;
  	}
  	if (end_x > MAX_X*GridScale - 1) {
  		end_x = MAX_X*GridScale - 1;
  	}
  	if (start_y < MIN_Y) {
  		start_y = MIN_Y;
  	}
  	if (end_y > MAX_Y*GridScale - 1) {
  		end_y = MAX_Y*GridScale - 1;
  	}
  	for (int j = start_x; j <= end_x; j++) {
  		for (int k = start_y; k <= end_y; k++) {
  			grid[j][k] = 1;
  		}
  	}
	std::cout << "StartX: " << start_x << " and ";
	std::cout << "EndX: " << end_x << " and ";
	std::cout << "StartY: " << start_y << " and ";
	std::cout << "EndY: " << end_y << "\n";
  }

  //Update the grid for boundaries
  for (int i = 0; i < MAX_X*GridScale; i++) {
  	for (int j = 0; j/GridScale < 1; j++) {
  		grid[i][j] = 1;
  	}
  }
  for (int i = 0; i < MAX_X*GridScale; i++) {
  	for (int j = MAX_Y*GridScale - 1; (MAX_Y*GridScale - 1 - j)/GridScale < 1; j--) {
  		grid[i][j] = 1;	
  	}
  }
  for (int i = 0; i < MAX_Y*GridScale; i++) {
  	for (int j = 0; j/GridScale < 1; j++) {
  		grid[j][i] = 1;	
  	}
  }
  for (int i = 0; i < MAX_Y*GridScale; i++) {
  	for (int j = MAX_X*GridScale - 1; (MAX_X*GridScale - 1 - j)/GridScale < 1; j--) {
  		grid[j][i] = 1;	
  	}
  }

  //Run BFS to determine a valid path between the vehicle_position and the goal_position
  BFS(vehicle_position*GridScale,goal_position*GridScale);
  final_path_x.push(vehicle_position.x()*GridScale);
  final_path_y.push(vehicle_position.y()*GridScale);
  next_position = vehicle_position;
}

// This method is called for each timestep of the simulation.  It should return the commanded
// acceleration vector for the vehicle.
// The path is already generated in the initialization stage, next_position is determined from this path considering the current vehicle_position
// and ComputeControl generates the accelaration 
Eigen::Vector2d ComputeControl(const Eigen::Vector2d& vehicle_position,
                               const Eigen::Vector2d& vehicle_velocity) {
	if (!bfs_flag)
		return {0.0, 0.0};
	float vpx = vehicle_position.x();
	float vpy = vehicle_position.y();
	if ((vpx - 0.1 < final_path_x.top()/GridScale && vpx + 0.1 > final_path_x.top()/GridScale) && (vpy - 0.1 < final_path_y.top()/GridScale && vpy + 0.1 > final_path_y.top()/GridScale)) {
	  	final_path_x.pop();
		next_position.x() = final_path_x.top()/GridScale;
		std::cout << "NextPositionX: " << next_position.x() << " and ";
		final_path_y.pop(); 
		next_position.y() = final_path_y.top()/GridScale;
		std::cout << "NextPositionY: " << next_position.y() << "\n";
	}
	float del_pos_x = next_position.x() - vehicle_position.x();
	float del_pos_y = next_position.y() - vehicle_position.y();
	Eigen::Vector2d acceleration;
	acceleration.x() = (2 * (del_pos_x - vehicle_velocity.x()) > MAX_ACCEL/sqrt(2)) ? MAX_ACCEL/sqrt(2) : 2 * (del_pos_x - vehicle_velocity.x());
	acceleration.y() = (2 * (del_pos_y - vehicle_velocity.y()) > MAX_ACCEL/sqrt(2)) ? MAX_ACCEL/sqrt(2) : 2 * (del_pos_y - vehicle_velocity.y());
  return acceleration;
}

int main () {
	std::vector<Eigen::Vector2d> obstacles;
	Eigen::Vector2d o1;
	o1.x() = 8.0;
	o1.y() = 8.0;
	Eigen::Vector2d vp;
	vp.x() = 2.5;
	vp.y() = 2.5;
	Eigen::Vector2d gp;
	gp.x() = 27.5;
	gp.y() = 27.5;
	obstacles.push_back(o1);
	o1.x() = 15.5;
	o1.y() = 24.7;
	obstacles.push_back(o1);
	Eigen::Vector2d vv;
	vv.x() = 1.0;
	vv.y() = 1.0;
	Initialize(vp,gp,obstacles);
	std:: cout << "ComputeControl: " << ComputeControl(vp, vv) << "\n";
	for (int i = 0; i < MAX_X*GridScale; i++) {
		for (int j = 0; j < MAX_Y*GridScale; j++) {
			std::cout << grid[i][j] << " ";
		}
		std:: cout << "\n";
	}
	return 0;
}
