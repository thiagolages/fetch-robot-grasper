#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion

def publisher():
    rospy.init_node("simple_publisher")
    pub = rospy.Publisher('/demo/pose_stamped',PoseStamped, queue_size=1)
    rate = rospy.Rate(1)

    # for wrist_roll_link
    #p1 = Pose( Point(0.042, 0.384, 1.826), Quaternion(0.173, -0.693, -0.242, 0.657) )
    #p2 = Pose( Point(0.047, 0.545, 1.822), Quaternion(-0.274, -0.701, 0.173, 0.635) )

    # for gripper_link
    #Translation: [0.041, 0.646, 1.954]
    #Rotation: in Quaternion [-0.279, -0.698, 0.171, 0.636]
    #p1 = Pose( Point(0.041, 0.646, 1.954), Quaternion(-0.279, -0.698, 0.171, 0.636) )
    p1 = Pose( Point(0.500, -0.205, 1.064), Quaternion(0.865, -0.298, -0.304, 0.265) )
    # Translation: [0.688, -0.205, 1.064]
    # Rotation: in Quaternion [0.865, -0.298, -0.304, 0.265]
    p2 = Pose( Point(0.688, -0.205, 1.064), Quaternion(0.865, -0.298, -0.304, 0.265) )

    
    count = 0
    while not rospy.is_shutdown():
        count = count + 1
        if count % 2 == 0:
            pose = p1
        else:
            pose = p2
        msg = PoseStamped()
        now = rospy.Time.now()#get_rostime()
        msg.header.stamp.secs = now.secs
        msg.header.stamp.nsecs = now.nsecs
        msg.header.frame_id = 'base_link'
        msg.pose = pose
        # msg.pose.position.x = 0.042
        # msg.pose.position.y = 0.384
        # msg.pose.position.z = 1.826
        # msg.pose.orientation.x = 0.173
        # msg.pose.orientation.y = -0.693
        # msg.pose.orientation.z = -0.242
        # msg.pose.orientation.w = 0.657
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass