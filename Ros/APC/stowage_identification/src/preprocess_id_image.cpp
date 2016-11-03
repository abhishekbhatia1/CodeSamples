#include <ros/ros.h>

#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>

#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>


#include <pcl/io/pcd_io.h>
#include <pcl/common/common.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl_ros/point_cloud.h>

#include "std_srvs/Empty.h"
#include "apc_msgs/pc_2img.h"
#include <opencv2/core/core.hpp>

#include <boost/filesystem.hpp>

#include <ctime>

using namespace cv;
using namespace std;

class CloudFilter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  ros::Subscriber kinect_cloud_sub_;
  image_transport::Subscriber kinect_image_sub_;
  ros::Publisher filter_kinect_image_pub_;
  cv_bridge::CvImagePtr cv_ptr;
  pcl::PointCloud <pcl::PointXYZRGB>::Ptr kinect_color;
  ros::ServiceServer service;
  pcl::PCDWriter writer;
  std::vector<int> params;
  Mat D;
    
public:
  CloudFilter()
    : it_(nh_)
  {
    // Subscrive to input video feed and publish output video feed
    kinect_image_sub_ = it_.subscribe("/IDkinect2/hd/image_color", 1,  &CloudFilter::imageCb, this);
    kinect_cloud_sub_ = nh_.subscribe("/IDkinect2/hd/points", 1, &CloudFilter::binCb, this); 
    filter_kinect_image_pub_ = nh_.advertise<sensor_msgs::Image>("/stowage_segmented_image", 1);
    kinect_color = pcl::PointCloud<pcl::PointXYZRGB>::Ptr(new pcl::PointCloud<pcl::PointXYZRGB>);
    service = nh_.advertiseService("preprocess_stowage_image", &CloudFilter::process, this);
    ROS_INFO("Ready to go");
    //mask_cloud = nh_.advertiseService("maskCloud", &CloudFilter::maskCloud, this);

    params.push_back(cv::IMWRITE_JPEG_QUALITY);
    params.push_back(100);
    params.push_back(cv::IMWRITE_PNG_COMPRESSION);
    params.push_back(1);
    params.push_back(cv::IMWRITE_PNG_STRATEGY);
    params.push_back(cv::IMWRITE_PNG_STRATEGY_RLE);
    params.push_back(0);

  }

  bool process(apc_msgs::pc_2img::Request&  req,
                 apc_msgs::pc_2img::Response& res)
  { 
    //std::cout << "FILTER CLOUD ID SERVICE CALLED" << "\n";
    //pcl::fromROSMsg(req.pcl_msg, *cloud_in);
    //cv_ptr = cv_bridge::toCvCopy(req.jpg_msg, sensor_msgs::image_encodings::RGB8);
    Mat image_init = cv_ptr->image;
    sensor_msgs::ImagePtr image_init_return = cv_bridge::CvImage(std_msgs::Header(), "bgr8", image_init).toImageMsg();
    res.img1 = *image_init_return;

    if (kinect_color->points.size()!=0)
    {


      for(int j = 0;j < cv_ptr->image.rows;j++){
        for(int i = 0;i < cv_ptr->image.cols;i++){
          //if ((j < 400 && i < 800) || (j > 700 && i > 1100))
          if (j > 200 && i > 400 && j < 800 && i < 1100) {
	    continue;
	  } else {
            int index_row = j;
            int index_col = i;
            if (index_col >=0 && index_col < cv_ptr->image.cols && index_row >= 0 &&  index_row < cv_ptr->image.rows) {
              cv_ptr->image.at<cv::Vec3b>(index_row,index_col)[0] = 0;
              cv_ptr->image.at<cv::Vec3b>(index_row,index_col)[1] = 0;
              cv_ptr->image.at<cv::Vec3b>(index_row,index_col)[2] = 0;
            }
          } 
        }
      }

      for (int i = 0; i < kinect_color->points.size(); i++) {
        if (!(kinect_color->points[i].z < 0.87)) {
          //int index_row = i/cv_ptr->image.cols;
          //int index_col = i - cv_ptr->image.cols * index_row;
          int index_row = (int) i / cv_ptr->image.cols;
          int index_col = (int) i % cv_ptr->image.cols;
          if (index_col >=0 && index_col < cv_ptr->image.cols && index_row >= 0 && index_row < cv_ptr->image.rows) {
            cv_ptr->image.at<cv::Vec3b>(index_row,index_col)[0] = 0;
            cv_ptr->image.at<cv::Vec3b>(index_row,index_col)[1] = 0;
            cv_ptr->image.at<cv::Vec3b>(index_row,index_col)[2] = 0;
          }
        }
      }

      //Mat difference;
      //threshold(cv_ptr->image, difference, 200, 255, CV_8UC1);
      Mat planes[3];
      split(cv_ptr->image,planes); 

      Moments m = moments(planes[0], false);
      Point p1(m.m10/m.m00, m.m01/m.m00);

      int size = 600;
      //cv::circle( cv_ptr->image, p1, 10, Scalar(0,0,255), 2 );
      //D = cv_ptr->image(Rect(p1.x-size/2+1, p1.y-size/2+1, size, size) );
      D = cv_ptr->image;
      sensor_msgs::ImagePtr img_msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", D).toImageMsg();
      res.img2 = *img_msg;

      if (not_empty_output_image())
      {
        std::cout << "PUB JPG" << "\n";
        publish_image();
      }
    } 


    // Save raw pc, filtered pc, raw image, filtered img
    int doSaveImages = 1;
    ros::param::get("doSaveImages", doSaveImages);
    std::cout << "checking to save images" <<std::endl;
    if( doSaveImages){
      std::string save_dir("/home/harp/stowage_data/");
      std::time_t now = time(0);
      std::tm *ltm = localtime(&now);
      std::string date_str;
      date_str.append(std::to_string(ltm->tm_mday));
      date_str.append(std::to_string(ltm->tm_hour));
      date_str.append(std::to_string(ltm->tm_min));
      date_str.append(std::to_string(ltm->tm_sec));

      const std::string raw_pc_name = save_dir +  date_str + "_raw.pcd";
      writer.writeBinary(raw_pc_name, *kinect_color);

      const std::string raw_img_name = save_dir +  date_str + "_raw.jpg";
      cv::imwrite(raw_img_name, image_init, params);
      const std::string filtered_img_name = save_dir +  date_str + "_filtered.jpg";
      cv::imwrite(filtered_img_name, D, params);

    }



    return true;
  }

  void publish_pointcloud();
  void publish_image();
  bool not_empty_output_image();
  void imageCb(const sensor_msgs::ImageConstPtr&);
  void binCb (const sensor_msgs::PointCloud2ConstPtr&);
};

void CloudFilter::publish_image()
{
  //std::cout << "Publishing Masked Image" << "\n" <<  std::flush;
  std::cout << "publishing\n";
  std::cout << "ROWS: " << D.rows << " COLS: " << D.cols << "\n";
  sensor_msgs::ImagePtr msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", D).toImageMsg();
  filter_kinect_image_pub_.publish(msg);
  std::cout << "published\n";
}


void CloudFilter::imageCb(const sensor_msgs::ImageConstPtr& msg)
{
  //std::cout << "GRABBED IMAGE" << "\n" <<  std::flush;
  try {
    cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("cv_bridge exception: %s", e.what());
    return;
  }
}


void CloudFilter::binCb (const sensor_msgs::PointCloud2ConstPtr& cloud_msg)
{
  //std::cout << "GRABBED kinect" << "\n" <<  std::flush;
  // Convert to PCL data type
  pcl::fromROSMsg(*cloud_msg, *kinect_color);
}


bool CloudFilter::not_empty_output_image()
{
  if (D.rows > 0 && D.cols > 0)
  {
    return true;
  }
  return false;
}


int main(int argc, char** argv)
{
  ros::init(argc, argv, "mask_shelf_pc");
  CloudFilter ic;

  ros::Rate loop_rate(1);
  while (ros::ok())
  {
    if (ic.not_empty_output_image())
    {
      std::cout << "PUB JPG" << "\n";
      ic.publish_image();
    }

    ros::spinOnce();
    loop_rate.sleep();
  }
  return 0;
}
