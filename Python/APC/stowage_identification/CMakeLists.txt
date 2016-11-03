cmake_minimum_required(VERSION 2.8.3)
project(stowage_identification)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11") 
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
set(CMAKE_BUILD_TYPE Release) 

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
    roscpp
    rospy
    std_msgs
    apc_msgs
    message_generation
    image_transport
    cv_bridge
    pluginlib 
    geometry_msgs
    pcl_conversions
    pcl_ros
    sensor_msgs
    std_srvs
    )


find_package(Boost COMPONENTS system filesystem date_time thread serialization mpi REQUIRED)
find_package(OpenCV)
find_package(MPI REQUIRED)
find_package(OpenMP)

include(CMakeForceCompiler)
CMAKE_FORCE_CXX_COMPILER(mpicxx ${CMAKE_CXX_COMPILER_ID})

#generate_messages(
#    DEPENDENCIES
#    std_msgs
#    geometry_msgs
#    sensor_msgs
#    )

catkin_package(
    #  INCLUDE_DIRS include
    CATKIN_DEPENDS 
    cv_bridge 
    pcl_ros 
    message_runtime
    DEPENDS
    OpenCV 
    PCL 
    Boost
    LIBRARIES
    )

include_directories(include 
  ${catkin_INCLUDE_DIRS}
  ${roscpp_INCLUDE_DIRS})
link_directories(${catkin_LIBRARY_DIRS})

include_directories(MPI_INCLUDE_PATH)
include_directories(include ${OpenCV_INCLUDE_DIRS})

# Add Libraries
# Can we move these to the catkin_package? LOL
add_library(ros_perception src/ros_perception.cpp)
target_link_libraries(ros_perception ${roscpp_LIBRARIES})

add_library(vision_tools src/vision_tools.cpp)
target_link_libraries(vision_tools ${catkin_LIBRARIES})

# Add Executables

add_executable(preprocess_id_image src/preprocess_id_image.cpp)
target_link_libraries(preprocess_id_image ${catkin_LIBRARIES})


