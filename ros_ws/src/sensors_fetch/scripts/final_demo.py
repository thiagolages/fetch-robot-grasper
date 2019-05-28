#!/usr/bin/env python

import rospy, math, tf2_ros, tf
import geometry_msgs.msg
from moveit_msgs.msg import MoveItErrorCodes
from moveit_python import MoveGroupInterface, PlanningSceneInterface
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion

from geometry_msgs.msg import Polygon

import moveit_commander
# class definition that is useful for moving base around (file inside our package)
from client_interface import MoveBaseClient 
from nav_msgs.msg import Path

path = Path()
p = Polygon()

def grasperCallback(gripper_pose_stamped):

    global move_group, group
    # This is the wrist link not the gripper itself
    #gripper_frame = 'wrist_roll_link'
    rospy.loginfo(gripper_pose_stamped)
    gripper_frame = 'gripper_link'
    #rospy.loginfo(gripper_pose_stamped)
    #rospy.loginfo("Moving %s to pose %s:\n",gripper_frame, gripper_pose_stamped.pose)

    # Moving gripper_frame to pose in gripper_pose_stamped's FRAME ID !
    # In this case, it means putting 'wrist_roll_link' into the pos/orientation
    # specified by gripper_pose_stamped.pose (which is in gripper_pose_stamped.header.frame_id coordinate frame)

    #move_group.moveToPose(gripper_pose_stamped, gripper_frame)
    #move_group.get_move_action().wait_for_result() #not tested
    #result = move_group.get_move_action().get_result()
    group.set_pose_target(gripper_pose_stamped)
    rospy.loginfo("before go()")
    rospy.loginfo("desired pose = %s",gripper_pose_stamped.pose)
    plan1 = group.go()
    rospy.loginfo("after go()")
    rospy.loginfo("current pose = %s",group.get_current_pose())


    '''
    if result:
           # Checking the MoveItErrorCode
           if result.error_code.val == MoveItErrorCodes.SUCCESS:
                rospy.loginfo("Nice !")
           else:
                # If you get to this point please search for:
                # moveit_msgs/MoveItErrorCodes.msg
                rospy.logerr("Arm goal in state: %s",
                             move_group.get_move_action().get_state())
    else:
            rospy.logerr("MoveIt! failure no result returned.")

    '''
    #if check_result(result):
    #    rospy.loginfo("Done !")
    #else:
    #    rospy.logerr("MoveIt! failure no result returned.")

def moveToJointPosition(joint_position):
    global move_group, group
    
    joints = ["shoulder_pan_joint", "shoulder_lift_joint", "upperarm_roll_joint",
              "elbow_flex_joint", "forearm_roll_joint", "wrist_flex_joint", "wrist_roll_joint"]

    rospy.loginfo("Moving to joint position %s:\n",joint_position)

    move_group.moveToJointPosition(joints, tuck_joint_pos)
    result = move_group.get_move_action().get_result()
    if check_result(result):
        rospy.loginfo("Done !")
        joint_pos = group.get_current_joint_values()
        rospy.loginfo("Current joint pos = %s",joint_pos)

def planning_scene_callback(data):
    global p
    return

def define_ground_plane():
    
    global p
    
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

    #rospy.Subscriber("/obstacles/table", PolygonWithHeight, planning_scene_callback)

    #while (p == None):
    #    continue

    # STOPPED HERE
    #size_x = polygon_with_height.polygon.points[0] - 
    #size_y = 
    #size_z = 
    #x = 
    #y = 
    #z = 
    #lanning_scene.addBox("table" , size_x=,size_x=,size_x=,x=,y=,z=) # avoid hitting the table

def check_result(result):
    global move_group

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
        rospy.logerr("aaaaaaaaaaaaaaaMoveIt! failure no result returned.")
        rospy.loginfo(result)

def grasper():
    
    rospy.Subscriber("/demo/pose_stamped", PoseStamped, grasperCallback)
    rospy.spin()

if __name__ == '__main__':

    rospy.init_node("final_demo")

    robot = moveit_commander.RobotCommander()
    group = moveit_commander.MoveGroupCommander("arm")
    planning_scene = PlanningSceneInterface("base_link")
    # Create move group interface for a fetch robot
    #move_group = MoveGroupInterface("arm_with_torso", "base_link") #moveToPose, moveToJointPosition, get_result
    move_group = MoveGroupInterface("arm", "base_link") #moveToPose, moveToJointPosition, get_result

    define_ground_plane()
    
    grasper()

    while not rospy.is_shutdown():
        continue

    # This stops all arm movement goals
    # It should be called when a program is exiting so movement stops
    move_group.get_move_action().cancel_all_goals()
