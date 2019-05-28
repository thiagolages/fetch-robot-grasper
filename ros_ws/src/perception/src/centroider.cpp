#include "perception/centroider.h"

#include "pcl/PointIndices.h"
#include "pcl/point_cloud.h"
#include "pcl/point_types.h"
#include "pcl_conversions/pcl_conversions.h"
#include "ros/ros.h"
#include "sensor_msgs/PointCloud2.h"

#include "pcl/filters/crop_box.h"
#include "pcl/common/common.h"
#include <visualization_msgs/Marker.h>
#include <geometry_msgs/PoseStamped.h>

#include <sstream>


typedef pcl::PointXYZRGB PointC;
typedef pcl::PointCloud<pcl::PointXYZRGB> PointCloudC;

namespace perception {

visualization_msgs::Marker marker;
geometry_msgs::PoseStamped pose_stamped;


void CentroidOfCloud(PointCloudC::Ptr cloud) {

	

	ROS_INFO("Got point cloud with %ld points", cloud->size());
	PointC min_pcl;
	PointC max_pcl;
	PointC centroid;
	pcl::getMinMax3D<PointC>(*cloud, min_pcl, max_pcl);
	centroid.x = 0.0;
	centroid.y = 0.0;
	centroid.z = 0.0;
	for (int i=0; i < int(cloud->size()); i++){
		centroid.x += cloud->at(i).x;
		centroid.y += cloud->at(i).y;
		centroid.z += cloud->at(i).z;
		ROS_INFO("cloud(%d) = %f", i, cloud->at(i).x);
		ROS_INFO("Centroid.x = %f", centroid.x);
	}
		centroid.x = centroid.x/cloud->size();
		centroid.y = centroid.y/cloud->size();
		centroid.z = centroid.z/cloud->size();
	
	ROS_INFO("Centroid: X: %f, Y: %f, Z: %f", centroid.x, centroid.y, centroid.z);


			//////////////////
			//MARKER
			//////////////////

					marker.header.frame_id = "head_camera_link";
					marker.header.stamp = ros::Time();
					marker.ns = "my_namespace";
					marker.id = 0;
					marker.type = visualization_msgs::Marker::SPHERE;
					marker.action = visualization_msgs::Marker::ADD;
					marker.pose.position.x = centroid.z;
					marker.pose.position.y = -centroid.x;
					marker.pose.position.z = -centroid.y;
					marker.pose.orientation.x = 0;
					marker.pose.orientation.y = 0;
					marker.pose.orientation.z = 0;
					marker.pose.orientation.w = 1.0;
					marker.scale.x = 0.05;
					marker.scale.y = 0.05;
					marker.scale.z = 0.05;
					marker.color.a = 1.0; // Don't forget to set the alpha!
					marker.color.r = 0.0;
					marker.color.g = 1.0;
					marker.color.b = 0.0;
					ROS_INFO("Updated Marker");

					pose_stamped.header = marker.header;
					pose_stamped.pose 	= marker.pose;
					ROS_INFO("Updated pose_stamped as well");

			//////////////////

			//////////////////
			//MARKER
			//////////////////

/*
					marker.header.frame_id = "head_camera_link";
					marker.header.stamp = ros::Time();
					marker.ns = "my_namespace";
					marker.id = 0;
					marker.type = visualization_msgs::Marker::SPHERE;
					marker.action = visualization_msgs::Marker::ADD;
					marker.pose.position.x = 0;
					marker.pose.position.y = 0;
					marker.pose.position.z = 0;
					marker.pose.orientation.x = 1;
					marker.pose.orientation.y = 1;
					marker.pose.orientation.z = 1;
					marker.pose.orientation.w = 1.0;
					marker.scale.x = 0.05;
					marker.scale.y = 0.05;
					marker.scale.z = 0.05;
					marker.color.a = 1.0; // Don't forget to set the alpha!
					marker.color.r = 0.0;
					marker.color.g = 1.0;
					marker.color.b = 0.0;
						ROS_INFO("Updated Marker");
			//////////////////
*/


}

Centroid_::Centroid_(const ros::Publisher& marker_pub, const ros::Publisher& pose_stamped_pub)
    : marker_pub_(marker_pub), pose_stamped_pub_(pose_stamped_pub) {}


void Centroid_::Callback(const sensor_msgs::PointCloud2& msg) {
  PointCloudC::Ptr cloud(new PointCloudC());
  pcl::fromROSMsg(msg, *cloud);
  CentroidOfCloud(cloud);
		 // sensor_msgs::PointCloud2 msg_out;
		 // pcl::toROSMsg(*cropped_cloud, msg_out);
  marker_pub_.publish(marker);
  pose_stamped_pub_.publish(pose_stamped);


}
}  // namespace perception
