#include <vector>

// Eigen is a C++ library for linear algebra (vectors, matrices, etc.).  We use it for the
// interfaces to the methods you are to implement, and we encourage you to use it in your
// implementation code as well.
// See: http://eigen.tuxfamily.org/
#include <Eigen/Dense>

// Bounds of the 2D area that is being simulated, in meters.  If the vehicle touches any of these
// boundaries, that is considered a crash.
#define MIN_X 0.0
#define MIN_Y 0.0
#define MAX_X 30.0
#define MAX_Y 30.0

// For collision checking purposes, the vehicle is treated as a circle with this radius in meters.
#define VEHICLE_RADIUS 0.7

// Obstacles are of this radius in meters.
#define OBSTACLE_RADIUS 1.0

// Vehicle is considered to have reached the goal if it touches a circle of this radius around
// the goal position.
#define GOAL_RADIUS 0.75

// The vehicle's velocity is clamped such that it will not exceed this velocity, in m/s.
#define MAX_VELOCITY 10.0

// If an attempt is made to command an acceleration larger than this (in m/s^2), the acceleration
// will be clamped to this magnitude.
#define MAX_ACCEL 10.0

// You should implement this method.  It is called once at the beginning of the simulation.
//
// vehicle_position - starting position of the vehicle
// goal_position - point that the vehicle is attempting to reach
// obstacles - list of obstacles which much be avoided (each of size OBSTACLE_RADIUS)
void Initialize(const Eigen::Vector2d& vehicle_position, const Eigen::Vector2d& goal_position,
                const std::vector<Eigen::Vector2d>& obstacles);

// You should implement this method.  It is called for each timestep of the simualation.  The
// vehicle's current position and velocity are provided to this method, and it is expected
// to return a 2D vector specifying the acceleration command which should be applied to the
// vehicle.  It is assumed that the vehicle can achieve this acceleration instantaneously.
Eigen::Vector2d ComputeControl(const Eigen::Vector2d& vehicle_position,
                               const Eigen::Vector2d& vehicle_velocity);
