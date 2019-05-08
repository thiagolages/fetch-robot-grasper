# fetch-robot-grasper

University of Technology Sydney, Australia.
Assignment for 41014 Sensors and Control for Mechatronic Systems subject, Autumn 2019 session

Group Members:
 - Jason Al Haddad 
 - Thiago Lages  (@thiagolages)
 - Zhaodong Wu 
 
Subject coordinator: Dr. Liang Zhao

## 1) Project Description: ##
Control the Fetch robot to grasp the object on the table, e.g. can of coke, box of cookies, using the robotic arm and hand by
using visual servoing method. Depth images and/or RGB images can be used for the visual servoing. The end-effector of the robot arm has been calibrated with the RGB-D camera.

Target: The Fetch robot grasps different interested objects on the table without falling down.

## 2) Installation ##

### 2.0) Ubuntu 14.04

The following proceures assume you have Ubuntu 14.04 LTS installed on your machine. Download it from the [releases page](http://releases.ubuntu.com/).
 
### 2.1) ROS Indigo Igloo

We will be using ROS Indigo Igloo. Follow the instructions at the [ROS Indigo installation instructions page.](http://wiki.ros.org/indigo/Installation/Ubuntu)

A summary of the commands is showed below:

1) `sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'`

2) `sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116`

3) `sudo apt-get update`

4) `sudo apt-get install ros-indigo-desktop-full`

5) `sudo rosdep init`

6) `rosdep update`

7) `echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc`

8) `source ~/.bashrc`

### 3) Fetch Robot

[Official documentation page](https://docs.fetchrobotics.com/).

#### 3.1) Install some dependent packages
`sudo apt-get install ros-indigo-opencv-candidate ros-indigo-costmap-2d ros-indigo-moveit-full`

#### 3.2) Install Gazebo simulator Demo
`sudo apt-get install ros-indigo-fetch-gazebo-demo`

#### 3.3) Install the main package from Fetch Robotics GitHub page

Go to your ROS workspace (which is called `ros_ws` here), and inside `ros_ws/src/`: 
1) `git clone https://github.com/fetchrobotics/fetch_ros`
2) `cd ..`
3) `catkin_make`
4) `source devel/setup.bash`

#### 3.4) Launch the simulator
`roslaunch fetch_gazebo simulation.launch`

It will be a long time (about 5 min depends on your network) to start the gazebo for the first time, as it downloads the model from internet.
#### 3.5) Check the data
`roslaunch fetch_gazebo playground.launch`
#### 3.6) pen another terminal
`roslaunch fetch_gazebo_demo demo.launch`
#### 3.7) Start rviz and add the depth/image/baselaser to your rviz.
`rviz`
