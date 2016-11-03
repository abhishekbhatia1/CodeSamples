// This is start of the header guard.  ADD_H can be any unique name.  By convention, we use the name of the header file.
#ifndef ROS_PERCEPTION_H
#define ROS_PERCEPTION_H

// Publish Segmented Bin
#include "ros/ros.h"
#include <pcl/io/pcd_io.h>
#include <string>
void publish_cloud(pcl::PointCloud<pcl::PointXYZRGB>::Ptr image, ros::Publisher pub, std::string frame);
void publish_cloud(pcl::PointCloud<pcl::PointXYZ>::Ptr image, ros::Publisher pub, std::string frame);

#endif
