#include "ros/ros.h"
#include "ros_perception.h" 
#include <pcl/io/pcd_io.h>
#include <pcl/common/common.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl_ros/point_cloud.h>
#include <string>

// Publish Segmeted Bin
void publish_cloud(pcl::PointCloud<pcl::PointXYZRGB>::Ptr image, ros::Publisher pub, std::string frame)
{
  sensor_msgs::PointCloud2 bin_msg;
  pcl::toROSMsg(*image, bin_msg);
  bin_msg.header.stamp = ros::Time::now();
  bin_msg.header.frame_id = frame;
  bin_msg.height = 1;
  bin_msg.width = image->points.size();
  pub.publish (bin_msg);
  return;  
}

void publish_cloud(pcl::PointCloud<pcl::PointXYZ>::Ptr image, ros::Publisher pub, std::string frame)
{
	pcl::PointCloud<pcl::PointXYZRGB>::Ptr image_new (new pcl::PointCloud<pcl::PointXYZRGB> ());
	pcl::copyPointCloud(*image, *image_new);
	publish_cloud(image_new, pub, frame);
	return;
}
