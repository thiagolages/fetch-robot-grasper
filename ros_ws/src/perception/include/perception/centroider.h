#include "pcl/PointIndices.h"
#include "pcl/point_cloud.h"
#include "pcl/point_types.h"
#include "ros/ros.h"
#include "sensor_msgs/PointCloud2.h"

namespace perception {
// Finds the largest horizontal surface in the given point cloud.
// This is useful for adding a collision object to MoveIt.
//
// Args:
//  cloud: The point cloud to extract a surface from.
//  indices: The indices of points in the point cloud that correspond to the
//    surface. Empty if no surface was found.
void CentroidOfCloud(pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud);

class Centroid_ {
 public:
  Centroid_(const ros::Publisher& marker_pub, const ros::Publisher& pose_stamped_pub);
  void Callback(const sensor_msgs::PointCloud2& msg);

 private:
  ros::Publisher marker_pub_, pose_stamped_pub_;
};
}  // namespace perception
