#!/usr/bin/env python

import rospy, math, tf2_ros, tf
import geometry_msgs.msg
from moveit_msgs.msg import MoveItErrorCodes
from moveit_python import MoveGroupInterface, PlanningSceneInterface
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

from geometry_msgs.msg import Polygon, PolygonStamped
from std_msgs.msg import Bool

import actionlib
from control_msgs.msg import PointHeadAction, PointHeadGoal

import moveit_commander
# class definition that is useful for moving base around (file inside our package)
from client_interface import MoveBaseClient 
from nav_msgs.msg import Path

from tf.transformations import quaternion_from_euler
from tf import TransformerROS, TransformListener
import tf2_ros

from math import sin, cos

path = Path()
table = PolygonStamped()


def grasperCallback(gripper_pose_stamped):

    global group

    rospy.loginfo(gripper_pose_stamped)
    gripper_frame = 'gripper_link'

    # Moving gripper_frame to pose in gripper_pose_stamped's FRAME ID !
    # In this case, it means putting 'wrist_roll_link' into the pos/orientation
    # specified by gripper_pose_stamped.pose (which is in gripper_pose_stamped.header.frame_id coordinate frame)
    group.set_pose_target(gripper_pose_stamped)
    rospy.loginfo("1) Desired pose = %s",gripper_pose_stamped.pose)
    result = group.plan()
    #print("result ================== %s",result)
    if (len(result.joint_trajectory.points) != 0):
        rospy.loginfo("SUCCESS on planning !")
        rospy.loginfo("Moving arm...")
        group.go(wait=True)
        group.stop() # no residual movement
        rospy.loginfo("Done moving arm !")
        group.clear_pose_targets()
        rospy.loginfo("2) Pose achieved = %s",group.get_current_pose())
    else:
        rospy.logerr("MoveIt! failure no result returned.")

    
    #rospy.loginfo("Error = %s",error)
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

def planningSceneCallback(polygon_stamped):
    global table
    #rospy.loginfo("Inside planningSceneCallback")
    table = polygon_stamped

def defineGroundPlane():
    
    global table
    
    # Define ground plane
    # This creates objects in the planning scene that mimic the ground
    # If these were not in place gripper could hit the ground
    
    rospy.loginfo("Defining obstacles around me..")

    global planning_scene
    planning_scene.removeCollisionObject("my_front_ground")
    planning_scene.removeCollisionObject("my_back_ground")
    planning_scene.removeCollisionObject("my_right_ground")
    planning_scene.removeCollisionObject("my_left_ground")
    planning_scene.removeCollisionObject("table")
    planning_scene.addCube("my_front_ground", 2,  1.1,  0.0, -1.0)
    planning_scene.addCube("my_back_ground" , 2, -1.2,  0.0, -1.0)
    planning_scene.addCube("my_left_ground" , 2,  0.0,  1.2, -1.0)
    planning_scene.addCube("my_right_ground", 2,  0.0, -1.2, -1.0)

    # se have a callback to update table

    #while not rospy.is_shutdown():
    print table
    if (len(table.polygon.points) > 0):
        rospy.loginfo("Received info related to the table !")
        #break    
    #    continue

        # STOPPED HERE
        max_x = max_y = max_z = -9999
        min_x = min_y = min_z =  9999
        for i in table.polygon.points:
            if i.x > max_x: max_x = i.x
            if i.y > max_y: max_y = i.y
            if i.z > max_z: max_z = i.z

            if i.x < min_x: min_x = i.x
            if i.y < min_y: min_y = i.y
            if i.z < min_z: min_z = i.z

        size_x = max_x - min_x
        size_y = max_y - min_y
        size_z = max_z - min_z
        
        p = PoseStamped()
        p.header = table.header
        p.pose.position.x = table.polygon.points[0].x
        p.pose.position.y = table.polygon.points[0].y
        p.pose.position.z = table.polygon.points[0].z
        p.pose.orientation.x = 0.0
        p.pose.orientation.y = 0.0
        p.pose.orientation.z = 0.0
        p.pose.orientation.w = 1.0
        rospy.loginfo("Point in previous reference frame = %s",p)
        
        #t = TransformListener()
        global t #TransformROS
        #buff = tf2_ros.Buffer()
        #t = tf2_ros.TransformListener(buff)

        #while not rospy.is_shutdown():
        #    try:
        #        new_p = t.transformPose('base_link', p)
        #        break
        #    except Exception as e:
        #        print (e)
        #        pass
        #x = new_p.pose.position.x
        #y = new_p.pose.position.y
        #z = new_p.pose.position.z
        #overriding just to test
        size_x = 1.0
        size_y = 1.0
        size_z = 0.1
        x = 1.0
        y = 0.0
        z = 1.0
        #rospy.loginfo("Point in NEW reference frame = %s",new_p)

        planning_scene.addBox("table" , size_x=size_x,size_y=size_y,size_z=size_z,x=x,y=y,z=z) # avoid hitting the table
    else:
        rospy.loginfo("Didn't receive information about the tabe yet, contonuing without adding table..")
    


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
        rospy.logerr("MoveIt! failure no result returned.")
        rospy.loginfo(result)

def grasper():
    
    rospy.Subscriber("/demo/centroid"   , PoseStamped, grasperCallback)    
    rospy.spin()

def initialMoveBase():
    pos = PoseStamped()
    rospy.loginfo("Moving base to a better position..")
    pos.header.frame_id = "map"
    pos.pose.position.x = 2.8
    pos.pose.position.y = 3.0
    pos.pose.position.z = 0.0
    pos.pose.orientation.x = 0.0
    pos.pose.orientation.y = 0.0
    pos.pose.orientation.z = 0.0
    pos.pose.orientation.w = 1.0
    moveBase(pos)

def initialLookAt():
    pos = PoseStamped()
    rospy.loginfo("Looking at the table..")
    pos.header.frame_id = "base_link"
    pos.pose.position.x = 1.0 
    pos.pose.position.y = 0.0
    pos.pose.position.z = 0.5
    pos.pose.orientation.x = 0.0
    pos.pose.orientation.y = 0.0
    pos.pose.orientation.z = 0.0
    pos.pose.orientation.w = 1.0
    lookAt(pos)

if __name__ == '__main__':

    rospy.init_node("final_demo")

    robot = moveit_commander.RobotCommander()
    group = moveit_commander.MoveGroupCommander("arm")
    planning_scene = PlanningSceneInterface("base_link")
    # Create move group interface for a fetch robot
    move_group = MoveGroupInterface("arm_with_torso", "base_link") #moveToPose, moveToJointPosition, get_result
    #move_group = MoveGroupInterface("arm", "base_link") #moveToPose, moveToJointPosition, get_result

    t =  TransformerROS()
    rospy.Subscriber("/convex_hull/output_polygon", PolygonStamped, planningSceneCallback)

    defineGroundPlane()
    
    #initialMoveBase()
    #initialLookAt()
    
    grasper()

    while not rospy.is_shutdown():
        continue

    # This stops all arm movement goals
    # It should be called when a program is exiting so movement stops
    move_group.get_move_action().cancel_all_goals()
