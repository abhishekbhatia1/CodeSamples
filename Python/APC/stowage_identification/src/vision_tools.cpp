#include <iostream>
#include "vision_tools.h" 
#include <boost/thread/thread.hpp>

#include <pcl/ModelCoefficients.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/features/normal_3d.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl/common/common.h>
#include <pcl/search/search.h>
#include <pcl/search/kdtree.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/registration/icp.h>
#include <pcl/keypoints/uniform_sampling.h>

Eigen::Affine3f get_random_rotation()
{
    Eigen::Affine3f transform = Eigen::Affine3f::Identity();
    float theta = (rand()%628)/100.0;
    float theta2 = (rand()%628)/100.0;
    float theta3 = (rand()%628)/100.0; 
    // The same rotation matrix as before; tetha radians arround Z axis
    transform.rotate (Eigen::AngleAxisf (theta, Eigen::Vector3f::UnitZ()));
    transform.rotate (Eigen::AngleAxisf (theta2, Eigen::Vector3f::UnitX()));
    transform.rotate (Eigen::AngleAxisf (theta3, Eigen::Vector3f::UnitY()));
    return(transform);
}

std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> cluster_scene(pcl::PointCloud<pcl::PointXYZ>::Ptr scene, float tol)
{
  // Creating the KdTree object for the search method of the extraction
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ>);
  tree->setInputCloud (scene);

  // Set Cluster Parameters
  std::vector<pcl::PointIndices> clusters;
  pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
  ec.setClusterTolerance (tol);
  ec.setMinClusterSize (25);
  ec.setMaxClusterSize (25000);
  ec.setSearchMethod (tree);
  ec.setInputCloud (scene);
  ec.extract (clusters);

  int numClusters = clusters.size ();
  size_t cube_number = 0;
  std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> cluster_vector;

  // Merge clusters onto vector
  for (size_t k = 0; k < numClusters; k++)
  {
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointIndices segmented_indices = clusters[k];

    for (size_t j = 0; j < segmented_indices.indices.size (); j++)
    {
      pcl::PointXYZ point = scene->points[segmented_indices.indices[j]];
      float x = point.x;
      float y = point.y;
      float z = point.z;
      cloud_cluster->points.push_back(point);
    }

    cloud_cluster->width = cloud_cluster->points.size ();
    cloud_cluster->height = 1;
    cloud_cluster->is_dense = true;
    cluster_vector.push_back(cloud_cluster);
  }
  return (cluster_vector);
}

// Creates single color point cloud for segmentation visualization
pcl::PointCloud<pcl::PointXYZRGB>::Ptr color_cloud (std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> scene_segmented)
{
  pcl::PointCloud<pcl::PointXYZRGB>::Ptr color_cloud (new pcl::PointCloud<pcl::PointXYZRGB>);
  for (size_t c=0; c<scene_segmented.size(); c++)
  {
    //std::cout << "HERE" << std::flush;
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr color_segment (new pcl::PointCloud <pcl::PointXYZRGB>);;
    pcl::copyPointCloud(*scene_segmented[c], *color_segment);
    int label = rand () % 8;
    // pack r/g/b into rgb
    uint8_t r = rand() % 255 + 1;
    uint8_t g = rand() % 255 + 1;
    uint8_t b = rand() % 255 + 1; 
    uint32_t rgb = ((uint32_t)r << 16 | (uint32_t)g << 8 | (uint32_t)b);
    //std::cout << "HERE" << std::flush;
    for (int j = 0; j < color_segment->points.size (); j++)
      color_segment->points[j].rgb = *reinterpret_cast<float*>(&rgb);
    *color_cloud = *color_cloud + *color_segment;
  }
  return color_cloud;  
}

// Find best matches between GT and model
std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> prune_scene(std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> cluster_vector_temp, int numItems)
{

  std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> cluster_vector;
  // Found too many clusters
  // Step 1: Merge clusters that overlap in the VERTICAL direction 
  if (cluster_vector_temp.size () > numItems)
  {
    size_t i=0;
    while((cluster_vector.size()<=numItems) && (i < cluster_vector_temp.size ()))
    {
      pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster1 = cluster_vector_temp[i];
      for (size_t j=i+1; j<cluster_vector_temp.size(); j++)
      {
        pcl::PointXYZ min_p1, max_p1;
        pcl::PointXYZ min_p2, max_p2;
        pcl::getMinMax3D(*cloud_cluster1, min_p1, max_p1);
        pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster2 = cluster_vector_temp[j];
        pcl::getMinMax3D(*cloud_cluster2, min_p2, max_p2);
        std::cout << "Min1 " << min_p1.x << " Max1 " << max_p1.x << " Min2 " << min_p2.x << " Max2 " << max_p2.x << "\n";
        if ( ((min_p1.x < max_p2.x) && (min_p1.x > min_p2.x))
              || ((max_p1.x < max_p2.x) && (max_p1.x > min_p2.x))
              || ((min_p1.x < min_p2.x) && (max_p1.x > max_p2.x)))
        {
          *cloud_cluster1 += *cloud_cluster2;
          cluster_vector_temp.erase(cluster_vector_temp.begin()+j);
          j = j - 1;
          std::cout << "MERGED CLUSTER  ";
        }
      }
      cluster_vector.push_back(cloud_cluster1);
      i = i+1;
    }
  }
  // Found correct number of clusters
  else
  {
    cluster_vector=cluster_vector_temp;
  }
 
  // Still too many clusters, remove the smallest ones
  while (cluster_vector.size() > numItems)
  {  
    size_t smallest_index = 0;
    size_t smallest_cluster = cluster_vector[0]->points.size();
    for (size_t i=0; i<cluster_vector.size(); i++)
    {
      if(cluster_vector[i]->points.size() < smallest_cluster)
      {
        smallest_cluster=cluster_vector[i]->points.size();
        smallest_index=i;
      }
    }  
    cluster_vector.erase(cluster_vector.begin()+smallest_index);
  }
  return cluster_vector;
}

std::vector<match_info> process_scene (std::vector<pcl::PointCloud<pcl::PointXYZ>::Ptr> clusters, std::vector<item_info> shelf_contents)
{
  // Predict matches between item and cluster
  std::vector<match_info> icp_results;

  for (size_t gt=0; gt<shelf_contents.size(); gt++)
  {
    pcl::PointCloud<pcl::PointXYZ>::Ptr ground_truth_input (new pcl::PointCloud<pcl::PointXYZ> ());
    ground_truth_input = shelf_contents[gt].model;

    for (size_t c=0; c<clusters.size(); c++)
    {
      float best_local_score = 0.0;
      Eigen::Matrix4f best_local_transform;

      pcl::PointCloud <pcl::PointXYZ>::Ptr scene_item (new pcl::PointCloud <pcl::PointXYZ>);
      pcl::copyPointCloud(*clusters[c], *scene_item);

      size_t i = 0;
      size_t max_inlier_ct = 0;

      match_info best_match_info;
      
      while (i<20)
      {
        i = i+1;

        pcl::PointCloud<pcl::PointXYZ>::Ptr scene_item_transformed_temp (new pcl::PointCloud <pcl::PointXYZ>);

        // Randomly perterb scene
        Eigen::Affine3f transform = get_random_rotation();
        pcl::transformPointCloud (*scene_item, *scene_item_transformed_temp, transform);

        Eigen::Affine3f transform2 = Eigen::Affine3f::Identity();   
        pcl::PointXYZ min_p, max_p;   
        pcl::getMinMax3D(*scene_item_transformed_temp, min_p, max_p);
        pcl::PointCloud<pcl::PointXYZ>::Ptr scene_item_transformed (new pcl::PointCloud <pcl::PointXYZ>);
        transform2.translation() << -(min_p.x+max_p.x)/2.0, -(min_p.y+max_p.y)/2.0, -(min_p.z+max_p.z)/2.0;;
        pcl::transformPointCloud (*scene_item_transformed_temp, *scene_item_transformed, transform2);

        pcl::IterativeClosestPoint<pcl::PointXYZ, pcl::PointXYZ> icp;      
        icp.setInputTarget(ground_truth_input);
        icp.setInputSource(scene_item_transformed);
        icp.setTransformationEpsilon (1e-8);
        icp.setEuclideanFitnessEpsilon (1e-8);
        icp.setMaxCorrespondenceDistance (1);
        icp.setMaximumIterations (50);

        pcl::PointCloud <pcl::PointXYZ>::Ptr scene_aligned (new pcl::PointCloud <pcl::PointXYZ>);
        icp.align(*scene_aligned);

        // Calculate matrix from GT to scene
        Eigen::Matrix4f M;
        Eigen::Matrix4f M2;
        M = transform.matrix();
        M2 = transform2.matrix();
        //std::cout << "\n" << icp.getFinalTransformation();
        M = icp.getFinalTransformation() * M2 * M;
        M = M.inverse().eval();

        // Count inliers based on matches from scene to GT
        size_t inlier_count = 0;
        float resolution = 128.0f;  
        pcl::octree::OctreePointCloudSearch<pcl::PointXYZ> octree (resolution);
        octree.setInputCloud (ground_truth_input);
        octree.addPointsFromInputCloud ();

        for (size_t pt=0; pt<scene_aligned->points.size(); pt++)
        {
          pcl::PointXYZ searchPoint = scene_aligned->points[pt];
          std::vector<int> pointIdxRadiusSearch;
          std::vector<float> pointRadiusSquaredDistance;
          float radius = .005;
          if (octree.radiusSearch (searchPoint, radius, pointIdxRadiusSearch, pointRadiusSquaredDistance) > 0)
          {      
            inlier_count = inlier_count+1;
          }
        } 

        // Transform GT to scene frame
        pcl::PointCloud <pcl::PointXYZ>::Ptr gt_transformed (new pcl::PointCloud <pcl::PointXYZ>);
        pcl::transformPointCloud (*ground_truth_input, *gt_transformed, M); 
        
        // Count outliers based on matches from GT to scene
        pcl::PointXYZ min_scene, max_scene;
        pcl::getMinMax3D(*scene_item, min_scene, max_scene);

        float delta = .01;
        float sMinX= min_scene.x - delta; float sMaxX= max_scene.x + delta;
        float sMinY= min_scene.y - delta; float sMaxY= max_scene.y + delta;
        float sMinZ = min_scene.z - delta; float sMaxZ = 2;

        size_t outlier_ct = 0;
        for (size_t i=0; i<gt_transformed->points.size(); i++)
        {
            if (gt_transformed->points[i].x > sMaxX || gt_transformed->points[i].x < sMinX ||
            gt_transformed->points[i].y > sMaxY || gt_transformed->points[i].y < sMinY ||
            gt_transformed->points[i].z > sMaxZ || gt_transformed->points[i].z < sMinZ )
            {
              outlier_ct = outlier_ct+1;
            }
        }
      
        // Calculate score based on inliers in scene and GT
        float outlier_score = 1 - ((1.0 * outlier_ct) / (gt_transformed->points.size()));
        float inlier_score =  (1.0 * inlier_count) / scene_item->points.size();    
        float score = outlier_score + inlier_score;
      
        if (score > best_local_score)
        {
          best_local_score = score;
          best_match_info.scene_cluster_index = c;
          best_match_info.ground_truth_index = gt;
          best_match_info.transform = M;
          best_match_info.match_score = score;
        }
      }
      icp_results.push_back(best_match_info);
    }
  }
  return icp_results;
}

Eigen::Matrix4f score_matches (std::vector<match_info> icp_results, int numItems)
{
  // Create score matrix
  Eigen::MatrixXf scoreMatrix (numItems, numItems);
  Eigen::Matrix4f best_transform;
  pcl::PointCloud<pcl::PointXYZ>::Ptr ground_truth_input (new pcl::PointCloud<pcl::PointXYZ> ());
  for (size_t i=0; i<icp_results.size(); i++)
  {
    scoreMatrix (icp_results[i].ground_truth_index, icp_results[i].scene_cluster_index) = icp_results[i].match_score;
  }

  std::cout << "Score Matrix: " << "\n";
  std::cout << scoreMatrix << "\n";

  float row_score_threshold = 1.5;  
  float zero_row_set = 0;

/*
  if (numItems > 1)
  {
    for (size_t i=0; i<numItems; i++) {
      float max_row_score = 0.0;
      for (size_t j=0; j<numItems; j++) {
        if (scoreMatrix(i, j) > max_row_score) max_row_score = scoreMatrix(i, j);
      }
      if (max_row_score < row_score_threshold) {
        zero_row_set = 1;
        for (size_t j=0; j<numItems; j++) {
          scoreMatrix(i, j) = 0;
        }
      }
    }
  }
*/      
  std::cout << "New Score Matrix: " << "\n";
  std::cout << scoreMatrix << "\n";

  size_t best_index = 0;
  float find_best_score = -1.0;

  // Minimize Score Matrix
  if (numItems == 1)
  {
    best_index = 0;
  }
  else if (numItems == 2)
  {
    for (size_t i=0; i<numItems; i++) {
      for (size_t j=0; j<numItems; j++) {
        if (i!=j) {
          float sum_score = scoreMatrix(0, i) + scoreMatrix(1, j);
          if (sum_score > find_best_score)
          {
            best_index = i;
            find_best_score = sum_score;
          }
        }
      }
    }
  }
  else if (numItems == 3)
  {
    for (size_t i=0; i<numItems; i++) {
      for (size_t j=0; j<numItems; j++) {
        for (size_t k=0; k<numItems; k++) {
          if ((i!=j) && (j!=k) && (k!=i)) {
            float sum_score = scoreMatrix(0, i) + scoreMatrix(1, j) + scoreMatrix(2, k);
            if (sum_score > find_best_score)
            {
              best_index = i;
              find_best_score = sum_score;
            }
          }
        }
      }
    }
  } 

  //ground_truth_input = ground_truth_ptrs[icp_results[best_index].ground_truth_index];
  find_best_score = icp_results[best_index].match_score;
  best_transform = icp_results[best_index].transform;   
  return best_transform;
}

// Project item onto shelf
pcl::PointCloud<pcl::PointXYZ>::Ptr projectItem (pcl::PointCloud<pcl::PointXYZ>::Ptr model, Eigen::Matrix4f M)
{
  pcl::PointCloud <pcl::PointXYZ>::Ptr gt_final (new pcl::PointCloud <pcl::PointXYZ>);
  pcl::transformPointCloud (*model, *gt_final, M);
  return gt_final;  
}

pcl::PointCloud<pcl::PointXYZ>::Ptr downsample (pcl::PointCloud<pcl::PointXYZ>::Ptr ground_truth_input)
{
    //  Downsample ground truth cloud
    pcl::PointCloud<pcl::PointXYZ>::Ptr ground_truth (new pcl::PointCloud<pcl::PointXYZ> ());
    pcl::UniformSampling<pcl::PointXYZ> uniform_sampling;
    uniform_sampling.setInputCloud (ground_truth_input);
    uniform_sampling.setRadiusSearch (0.005f);

    pcl::PointCloud<int> keypointIndices;
    uniform_sampling.compute(keypointIndices);
    pcl::copyPointCloud(*ground_truth_input, keypointIndices.points, *ground_truth);
    return (ground_truth);
}
