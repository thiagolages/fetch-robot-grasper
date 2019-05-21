#!/usr/bin/env python

import rospy, math, tf2_ros
import geometry_msgs.msg
from moveit_msgs.msg import MoveItErrorCodes
from moveit_python import MoveGroupInterface, PlanningSceneInterface
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion

import moveit_commander
# class definition that is useful for moving base around (file inside our package)
from client_interface import MoveBaseClient 

# def get_relative_pose():

# 	tfBuffer = tf2_ros.Buffer()
# 	listener = tf2_ros.TransformListener(tfBuffer)


# 	turtle_vel = rospy.Publisher('/cmd_vel' % turtle_name, geometry_msgs.msg.Twist, queue_size=1)
# 	rate = rospy.Rate(10.0)
# 	try:
# 	    trans = tfBuffer.lookup_transform('', '/map', rospy.Time())
# 	except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
# 	    rate.sleep()
# 	    continue

# 	msg = geometry_msgs.msg.Twist()
# 	msg.angular.z = 4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
# 	msg.linear.x = 0.5 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2)
# 	turtle_vel.publish(msg)



def moveToPose(gripper_poses):
    
    # This is the wrist link not the gripper itself
    gripper_frame = 'wrist_roll_link'

    # Construct a "pose_stamped" message as required by moveToPose
    gripper_pose_stamped = PoseStamped()
    gripper_pose_stamped.header.frame_id = 'base_link'

    for pose in gripper_poses:
        rospy.loginfo("Moving to pose %s:\n",pose)
        #rospy.loginfo("Inside 'pose' loop")
        # Finish building the Pose_stamped message
        gripper_pose_stamped.header.stamp = rospy.Time.now()
        gripper_pose_stamped.pose = pose

        # Move gripper frame to the pose specified
        move_group.moveToPose(gripper_pose_stamped, gripper_frame)
        result = move_group.get_move_action().get_result()

        if check_result(result):
            rospy.loginfo("Done !")
            #joint_pos = group.get_current_joint_values()
            #rospy.loginfo("Current joint pos = ",joint_pos)

def moveToJointPosition(joint_position):
    global move_group, joints, group
    
    rospy.loginfo("Moving to joint position %s:\n",joint_position)

    move_group.moveToJointPosition(joints, tuck_joint_pos)
    result = move_group.get_move_action().get_result()
    if check_result(result):
        rospy.loginfo("Done !")
        joint_pos = group.get_current_joint_values()
        rospy.loginfo("Current joint pos = %s",joint_pos)


#def lower_torso():


def define_ground_plane():
    # Define ground plane
    # This creates objects in the planning scene that mimic the ground
    # If these were not in place gripper could hit the ground
    global planning_scene
    
    planning_scene.removeCollisionObject("my_front_ground")
    planning_scene.removeCollisionObject("my_back_ground")
    planning_scene.removeCollisionObject("my_right_ground")
    planning_scene.removeCollisionObject("my_left_ground")
    planning_scene.addCube("my_front_ground", 2,  1.1,  0.0, -1.0)
    planning_scene.addCube("my_back_ground" , 2, -1.2,  0.0, -1.0)
    planning_scene.addCube("my_left_ground" , 2,  0.0,  1.2, -1.0)
    planning_scene.addCube("my_right_ground", 2,  0.0, -1.2, -1.0)

    #planning_scene.addCube("my_front_plane" , 2,  0.5, 0.0, 1.0) # avoid hitting the table

def check_result(result):
    if result:
        # Checking the MoveItErrorCode
        if result.error_code.val == MoveItErrorCodes.SUCCESS:
            return True
        else:
            # If you get to this point please search for:
            # moveit_msgs/MoveItErrorCodes.msg
            rospy.logerr("Arm goal in state: %s",
            move_group.get_move_action().get_state())
            return False
    else:
        rospy.logerr("MoveIt! failure no result returned.")


# Note: fetch_moveit_config move_group.launch must be running
# Safety!: Do NOT run this script near people or objects.
# Safety!: There is NO perception.
#          The ONLY objects the collision detection software is aware
#          of are itself & the floor.
if __name__ == '__main__':

    # More info
    # http://docs.ros.org/kinetic/api/moveit_tutorials/html/doc/move_group_python_interface/move_group_python_interface_tutorial.html
    
    rospy.init_node("simple_task_world_coordinate")
    
    print("HEEEEELLO")
    
    planning_scene = PlanningSceneInterface("base_link")

    define_ground_plane()
    
    # Create move group interface for a fetch robot
    move_group = MoveGroupInterface("arm_with_torso", "base_link")
    move_base  = MoveBaseClient()

    # If we want to move the robot around
    #position = [2.250, 3.118,  1.57]
    #position = [4.050, 4.050, -1.57]
    #rospy.loginfo("Moving to a different position")
    #move_base.goto(position[0], position[1], position[2])
    
    # Position and rotation of two "wave end poses"
    p1 = Pose( Point(0.042, 0.384, 1.826), Quaternion(0.173, -0.693, -0.242, 0.657) )
    p2 = Pose( Point(0.047, 0.545, 1.822), Quaternion(-0.274, -0.701, 0.173, 0.635) )
    gripper_poses = [p1, p2]

    tuck_joint_pos = [1.32, 1.40, -0.2, 1.72, 0.0, 1.66, 0.0]
    joints = ["shoulder_pan_joint", "shoulder_lift_joint", "upperarm_roll_joint",
                  "elbow_flex_joint", "forearm_roll_joint", "wrist_flex_joint", "wrist_roll_joint"]
    robot = moveit_commander.RobotCommander()
    group = moveit_commander.MoveGroupCommander("arm")

    # To get the robot full curent state:
    #current_state = robot.get_current_state()
    #print ("============ Printing robot state")
    #print(current_state)
    #print ("============")

    # To get just joint angles:
    #group_variable_values = group.get_current_joint_values()
    #print "============ Joint values: ", group_variable_values


    while not rospy.is_shutdown():
	   
        rospy.loginfo("Now shaking arm")
        moveToPose(gripper_poses)

        rospy.loginfo("Now tucking arm")
        moveToJointPosition(tuck_joint_pos)

        rospy.sleep(3)

    # This stops all arm movement goals
    # It should be called when a program is exiting so movement stops
    move_group.get_move_action().cancel_all_goals()
