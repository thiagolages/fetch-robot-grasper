#!/usr/bin/env python

import rospy, math, tf
import geometry_msgs.msg
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


from math import sin, cos
class MoveBaseClient(object):

    def __init__(self):
        self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base...")
        self.client.wait_for_server()

    def goto(self, x, y, theta, frame="map"):
        rospy.loginfo("Moving..")
        move_goal = MoveBaseGoal()
        move_goal.target_pose.pose.position.x = x
        move_goal.target_pose.pose.position.y = y
        move_goal.target_pose.pose.orientation.z = sin(theta/2.0)
        move_goal.target_pose.pose.orientation.w = cos(theta/2.0)
        move_goal.target_pose.header.frame_id = frame
        move_goal.target_pose.header.stamp = rospy.Time.now()

        # TODO wait for things to work
        self.client.send_goal(move_goal)
        self.client.wait_for_result()
        rospy.loginfo("Done !")

def moveBaseCallback(msg):
    # doing this so we have a callback and also a 'standalone' function inside the code to move the base to whereever we want
    moveBase(msg)

def moveBase(pose_stamped):
    move_base = MoveBaseClient()
    move_base.goto(pose_stamped.pose.position.x, pose_stamped.pose.position.y, pose_stamped.pose.orientation.z, 
                    frame=pose_stamped.header.frame_id)

def lookAtCallback(msg):
    # doing this so we have a callback and also a 'standalone' function inside the code to look_at whatever we want
    rospy.loginfo("inside LOOKATCALLBACK")
    lookAt(msg)

def lookAt(pose_stamped):
    rospy.loginfo("Received at lookAt == %s",pose_stamped)
    client = actionlib.SimpleActionClient("head_controller/point_head", PointHeadAction)
    rospy.loginfo("Waiting for head_controller...")
    client.wait_for_server()
    rospy.loginfo("Done waiting !")
    goal = PointHeadGoal()
    goal.target.header.stamp = rospy.Time.now()
    goal.target.header.frame_id = pose_stamped.header.frame_id
    goal.target.point.x = pose_stamped.pose.position.x
    goal.target.point.y = pose_stamped.pose.position.y
    goal.target.point.z = pose_stamped.pose.position.z
    duration = 1.0
    goal.min_duration = rospy.Duration(duration)
    client.send_goal(goal)
    client.wait_for_result()

def lowerTorsoCallback(data):
    # doing this so we have a callback and also a 'standalone' function inside the code to lower the torso whenever we want
    lower_torso(data.data) # either 0 or 1

def lower_torso(option):
    
    if option: # if we want to lower it
        rospy.loginfo("Lowering torso..")
        torso_action = FollowTrajectoryClient("torso_controller", ["torso_lift_joint"])
        torso_action.move_to([0.0, ])
        rospy.loginfo("Done lowering torso !")
    else:
        rospy.loginfo("Keeping torso in the same position.")

def tuckCallback(data):
    # doing this so we have a callback and also a 'standalone' function inside the code to tuck it whenever we want
    tuck(data.data) # either 0 or 1

def tuck(option):

    global group

    joints = ["shoulder_pan_joint", "shoulder_lift_joint", "upperarm_roll_joint",
              "elbow_flex_joint", "forearm_roll_joint", "wrist_flex_joint", "wrist_roll_joint"]
    joint_pose = [1.32, 1.40, -0.2, 1.72, 0.0, 1.66, 0.0]
    
    if option:
        while not rospy.is_shutdown():
            result = group.go(joint_pose)
            if result:
                rospy.loginfo("Tucking..")
                group.go(joint_pose, wait=True)
                group.stop() # no residual movement
                rospy.loginfo("Done Tucking !")
                return
    else:
        rospy.loginfo("Keeping arm in the same position (not executing tuck command).")


def control():
    
    rospy.loginfo("Initializing topics to control base, torso, head, tuck, and to receive centroid..")
    rospy.Subscriber("/demo/tuck"       , Bool       , tuckCallback)
    rospy.Subscriber("/demo/lower_torso", Bool       , lowerTorsoCallback)
    rospy.Subscriber("/demo/look_at"    , PoseStamped, lookAtCallback)
    rospy.Subscriber("/demo/move_base"  , PoseStamped, moveBaseCallback)
    rospy.loginfo("Done !")
    rospy.spin()

if __name__ == '__main__':

    rospy.init_node("robot_manual_control")
    
    robot = moveit_commander.RobotCommander()
    group = moveit_commander.MoveGroupCommander("arm")
    
    control()