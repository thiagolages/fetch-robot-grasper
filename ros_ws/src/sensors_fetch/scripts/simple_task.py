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

def moveToPose(gripper_poses):

    global move_group
    # This is the wrist link not the gripper itself
    gripper_frame = 'wrist_roll_link'
    #gripper_frame = 'gripper_link'
    listener = tf.TransformListener()

    # Construct a "pose_stamped" message as required by moveToPose
    gripper_pose_stamped = PoseStamped()

    

    for pose in gripper_poses:
        gripper_pose_stamped.pose = pose
        gripper_pose_stamped.header.stamp = rospy.Time.now()
        gripper_pose_stamped.header.frame_id = 'base_link'
      
        flag = True
        '''
        #change before moving
        while(flag == True):
            try: 
                gripper_pose_stamped.pose = pose  
                rospy.loginfo("Pelo menos entrei")
                t = tf.TransformerROS() 
                (trans, rot) = listener.lookupTransform('/wrist_roll_link','/gripper_link',rospy.Time(0))
                #new_pose = listener.transformPose('/base_link', gripper_pose_stamped)
                mat_tf   = t.fromTranslationRotation(trans, rot)
                mat_pose = t.fromTranslationRotation(pose.translation, pose.rotation)
                pose = mat * pose
                
                rospy.loginfo("Moving %s to pose %s:\n",gripper_frame, pose)
                rospy.loginfo("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                #flag = False
            except Exception, e:
                from traceback import print_exc
                print 'type is:', e.__class__.__name__
                print_exc()
                rospy.loginfo("Sem tempo irmao")
                continue
        ''' #comentado


        rospy.loginfo("Moving %s to pose %s:\n",gripper_frame, pose)
        #rospy.loginfo("Inside 'pose' loop")
        # Finish building the Pose_stamped message


        # Moving gripper_frame to pose in gripper_pose_stamped's FRAME ID !
        # In this case, it means putting 'wrist_roll_link' into the pos/orientation
        # specified by gripper_pose_stamped.pose (which is in gripper_pose_stamped.header.frame_id coordinate frame)
        move_group.moveToPose(gripper_pose_stamped, gripper_frame)
        result = move_group.get_move_action().get_result()

        if check_result(result):
            rospy.loginfo("Done !")
            while not rospy.is_shutdown(): #fake loop, just until we get a valid tf
                try:
                    
                    #(trans,rot) = listener.lookupTransform('/base_link','/wrist_roll_link',rospy.Time(0))
                    (trans,rot) = listener.lookupTransform('/base_link','/gripper_link',rospy.Time(0))
                    rospy.loginfo("tf: RECEIVED. Creating a Path for visualization")
                    global path
                    '''
                    path.header.stamp = rospy.Time(0)
                    pose = PoseStamped()
                    pose.header.stamp = rospy.Time.now() 
                    pose.header.frame_id = 'gripper_link'
                    pose.pose.position.x = trans[0]
                    pose.pose.position.y = trans[1]
                    pose.pose.position.z = trans[2]
                    pose.pose.orientation.x = rot[0]
                    pose.pose.orientation.y = rot[1]
                    pose.pose.orientation.z = rot[2]
                    pose.pose.orientation.w = rot[3]
                    rospy.loginfo("path")
                    rospy.loginfo(path)
                    path.poses.append(pose)
                    path_pub = rospy.Publisher('/test_path', Path, queue_size=10)
                    path_pub.publish(path)
                    '''

                    msg = PoseStamped()
                    msg.header.frame_id = 'base_link'
                    msg.header.stamp = rospy.Time(0)
                    msg.pose.position.x = trans[0]
                    msg.pose.position.y = trans[1]
                    msg.pose.position.z = trans[2]
                    msg.pose.orientation.x = rot[0]
                    msg.pose.orientation.y = rot[1]
                    msg.pose.orientation.z = rot[2]
                    msg.pose.orientation.w = rot[3]
                    rospy.loginfo("TF base = %s",msg.pose)

                    
                    p_in_base = listener.transformPose("/base_link", msg)
                    print ('\n\n p_in_base \n\n %s',p_in_base)

                    #exit()
                    break
                except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                    rospy.loginfo("tf: nothing received")
                    continue
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

def planning_scene_callback(data):
    global p
    return

p = Polygon()

def define_ground_plane():
    
    global p
    
    # Define ground plane
    # This creates objects in the planning scene that mimic the ground
    # If these were not in place gripper could hit the ground
    
    planning_scene = PlanningSceneInterface("base_link")
    planning_scene.removeCollisionObject("my_front_ground")
    planning_scene.removeCollisionObject("my_back_ground")
    planning_scene.removeCollisionObject("my_right_ground")
    planning_scene.removeCollisionObject("my_left_ground")
    planning_scene.addCube("my_front_ground", 2,  1.1,  0.0, -1.0)
    planning_scene.addCube("my_back_ground" , 2, -1.2,  0.0, -1.0)
    planning_scene.addCube("my_left_ground" , 2,  0.0,  1.2, -1.0)
    planning_scene.addCube("my_right_ground", 2,  0.0, -1.2, -1.0)

    #rospy.Subscriber("/obstacles/table", PolygonWithHeight, planning_scene_callback)

    #while (polygon_with_height.height == None):
    #    continue

    # STOPPED HERE
    #size_x = polygon_with_height.polygon.points[0] - 
    #size_y = 
    #size_z = 
    #x = 
    #y = 
    #z = 
    #lanning_scene.addBox("table" , size_x=,size_x=,size_x=,x=,y=,z=) # avoid hitting the table

def move_around():
    
    move_base  = MoveBaseClient()

    position = [2.250, 3.118,  1.57]
    position = [4.050, 4.050, -1.57]
    rospy.loginfo("Moving to a different position")
    move_base.goto(position[0], position[1], position[2])

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

if __name__ == '__main__':

    # Note: fetch_moveit_config move_group.launch must be running
    # Safety!: Do NOT run this script near people or objects.
    # Safety!: There is NO perception.
    #          The ONLY objects the collision detection software is aware
    #          of are itself & the floor.

    # More info
    # http://docs.ros.org/kinetic/api/moveit_tutorials/html/doc/move_group_python_interface/move_group_python_interface_tutorial.html
    
    rospy.init_node("simple_task_world_coordinate")

    #### TEST #######
    #get_relative_pose()
    ###########
    robot = moveit_commander.RobotCommander()
    group = moveit_commander.MoveGroupCommander("arm")
    
    # Create move group interface for a fetch robot
    move_group = MoveGroupInterface("arm_with_torso", "base_link") #moveToPose, moveToJointPosition, get_result

    define_ground_plane()
    
    # If we want to move the robot around
    #move_around()
    
    # Position and rotation of two "wave end poses"
    p1 = Pose( Point(0.042, 0.384, 1.826), Quaternion(0.173, -0.693, -0.242, 0.657) )
    p2 = Pose( Point(0.047, 0.545, 1.822), Quaternion(-0.274, -0.701, 0.173, 0.635) )
    #gripper_poses = [p1, p2]
    gripper_poses = [p2, p1]

    tuck_joint_pos = [1.32, 1.40, -0.2, 1.72, 0.0, 1.66, 0.0]
    joints = ["shoulder_pan_joint", "shoulder_lift_joint", "upperarm_roll_joint",
                  "elbow_flex_joint", "forearm_roll_joint", "wrist_flex_joint", "wrist_roll_joint"]
    
    # To get the robot full curent state:
    #current_state = robot.get_current_state()
    #print ("============ Printing robot state")
    #print(current_state)
    #print ("============")

    # To get just joint angles:
    #group_variable_values = group.get_current_joint_values()
    #print "============ Joint values: ", group_variable_values


    while not rospy.is_shutdown():
        rospy.loginfo("referece frame = %s", group.get_planning_frame())
        rospy.loginfo("Now shaking arm")
        moveToPose(gripper_poses)
        rospy.loginfo("DONE shaking arm")

        #rospy.loginfo("Now tucking arm")
        #moveToJointPosition(tuck_joint_pos)

        rospy.sleep(3)

    # This stops all arm movement goals
    # It should be called when a program is exiting so movement stops
    move_group.get_move_action().cancel_all_goals()
