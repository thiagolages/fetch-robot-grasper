#include "perception/segmentation.h"
#include "ros/ros.h"
#include "sensor_msgs/PointCloud2.h"
#include <visualization_msgs/Marker.h>

int main(int argc, char** argv) {
  ros::init(argc, argv, "point_cloud_demo");
  ros::NodeHandle nh;
  ros::Publisher table_pub =
      nh.advertise<visualization_msgs::Marker>("centroid_marker", 1, true);
  perception::Segmenter segmenter(table_pub);
  ros::Subscriber sub =
      nh.subscribe("cloud_in", 1, &perception::Segmenter::Callback, &segmenter);
  ros::spin();
  return 0;
}
