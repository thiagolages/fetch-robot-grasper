#include "perception/crop.h"
#include "ros/ros.h"
#include "sensor_msgs/PointCloud2.h"
#include "pcl_conversions/pcl_conversions.h"
#include "pcl/filters/crop_box.h"
#include "pcl/common/common.h"
#include <visualization_msgs/Marker.h>

#include "std_msgs/String.h"
#include <sstream>

typedef pcl::PointXYZRGB PointC;
typedef pcl::PointCloud<pcl::PointXYZRGB> PointCloudC;

namespace perception {

Cropper::Cropper() {}

//	sensor_msgs::PointCloud2 output_centroid;

visualization_msgs::Marker marker;

	void Cropper::Callback(const sensor_msgs::PointCloud2& msg) {


	PointCloudC::Ptr cloud(new PointCloudC());
	pcl::fromROSMsg(msg, *cloud);
	ROS_INFO("Got point cloud with %ld points", cloud->size());
	PointC min_pcl;
	PointC max_pcl;
	PointC centroid;
	pcl::getMinMax3D<PointC>(*cloud, min_pcl, max_pcl);
	centroid.x=min_pcl.x + max_pcl.x/2;
	centroid.y=min_pcl.y + max_pcl.y/2;
	centroid.z=min_pcl.z + max_pcl.z/2;
	ROS_INFO("Centroid: X: %f, Y: %f, Z: %f", centroid.x, centroid.y, centroid.z);

	//pcl::toROSMsg(*centroid, output_centroid);

/*

  ros::NodeHandle node_handle;
ros::Publisher vis_pub = node_handle.advertise<visualization_msgs::Marker>( "origin", 0 );

visualization_msgs::Marker origin;
origin.header.frame_id = "base_link";
origin.header.stamp = ros::Time();
origin.ns = "my_namespace";
origin.id = 0;
origin.type = visualization_msgs::Marker::SPHERE;
origin.action = visualization_msgs::Marker::ADD;
origin.pose.position.x = 1;
origin.pose.position.y = 1;
origin.pose.position.z = 1;
origin.pose.orientation.x = 0.0;
origin.pose.orientation.y = 0.0;
origin.pose.orientation.z = 0.0;
origin.pose.orientation.w = 1.0;
origin.scale.x = 1;
origin.scale.y = 0.1;
origin.scale.z = 0.1;
origin.color.a = 1.0; // Don't forget to set the alpha!
origin.color.r = 0.0;
origin.color.g = 1.0;
origin.color.b = 0.0;

vis_pub.publish( origin );

*/
//////////////////
//MARKER
//////////////////

marker.header.frame_id = "base_link";
marker.header.stamp = ros::Time();
marker.ns = "my_namespace";
marker.id = 0;
marker.type = visualization_msgs::Marker::SPHERE;
marker.action = visualization_msgs::Marker::ADD;
marker.pose.position.x = 1;
marker.pose.position.y = 1;
marker.pose.position.z = 1;
marker.pose.orientation.x = centroid.x;
marker.pose.orientation.y = centroid.y;
marker.pose.orientation.z = centroid.z;
marker.pose.orientation.w = 1.0;
marker.scale.x = 1;
marker.scale.y = 0.1;
marker.scale.z = 0.1;
marker.color.a = 1.0; // Don't forget to set the alpha!
marker.color.r = 0.0;
marker.color.g = 1.0;
marker.color.b = 0.0;
	ROS_INFO("Updated Marker");
//////////////////




	}

int main(int argc, char** argv)
{
  ros::init(argc, argv, "visualization_marker");
  ros::NodeHandle n;
 // ros::Publisher centroid_pub = n.advertise<sensor_msgs::PointCloud2>("output_centroid", 1, true);
  ros::Publisher vis_pub = n.advertise<visualization_msgs::Marker>( "visualization_marker", 1, true);
  ros::Rate loop_rate(10);
vis_pub.publish(marker);
  int count = 0;
  while (ros::ok())
  {

vis_pub.publish(marker);
 //   centroid_pub.publish(output_centroid);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}




}
