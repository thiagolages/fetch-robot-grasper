#include "perception/centroider.h"
#include "ros/ros.h"
#include "sensor_msgs/PointCloud2.h"
#include <visualization_msgs/Marker.h>
#include <geometry_msgs/PoseStamped.h>

int main(int argc, char** argv) {
  ros::init(argc, argv, "point_cloud_demo");
  ros::NodeHandle nh;
  ros::Publisher marker_pub =
      nh.advertise<visualization_msgs::Marker>("centroid_marker", 1, true);
  ros::Publisher pose_stamped_pub =
      nh.advertise<geometry_msgs::PoseStamped>("/demo/centroid", 1, true);
  perception::Centroid_ centroid_(marker_pub, pose_stamped_pub);
  ros::Subscriber sub =
      nh.subscribe("cloud_in", 1, &perception::Centroid_::Callback, &centroid_);
  ros::spin();
  return 0;
}
