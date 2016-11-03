// This is start of the header guard.  ADD_H can be any unique name.  By convention, we use the name of the header file.
#ifndef VISION_TOOLS_H
#define VISION_TOOLS_H

#include <pcl/io/pcd_io.h>

struct item_info {
  int item_number;
  bool item_of_interest;
  pcl::PointCloud<pcl::PointXYZ>::Ptr model;
};

struct match_info {
  int scene_cluster_index;
  int ground_truth_index;
  Eigen::Matrix4f transform;
  float match_score;
};


// Segments scene, w/o enforcing number of clusters
// Outputs a vector of point clouds
#include <vector>
std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> cluster_scene(pcl::PointCloud<pcl::PointXYZ>::Ptr scene, float tol);

// Creates single color point cloud for segmentation visualization
pcl::PointCloud<pcl::PointXYZRGB>::Ptr color_cloud (std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> scene_segmented);

// Tries to properly enforce # of clusters 
std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> prune_scene(std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> cluster_vector_temp, int numItems);

// Does ICP for each GT and item pair 
std::vector<match_info> process_scene (std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> clusters, std::vector<item_info> shelf_contents);

// Minimizes score matrix
Eigen::Matrix4f score_matches (std::vector<match_info> icp_results, int numItems);

// Project item onto shelf
pcl::PointCloud<pcl::PointXYZ>::Ptr projectItem (pcl::PointCloud<pcl::PointXYZ>::Ptr model, Eigen::Matrix4f M);

// Downsample point cloud
pcl::PointCloud<pcl::PointXYZ>::Ptr downsample (pcl::PointCloud<pcl::PointXYZ>::Ptr ground_truth_input);

// Takes a segmented shelf and the set of ground truth images
// Estimates transformation from ground truth to scene
// ToDo Fix output
// Also maybe output score or score matrix?
//void process_scene (std::vector<item_info> shelf_contents, std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> scene_segmented);

// This is the end of the header guard
#endif
