# Install script for directory: /media/thiago/138f6b25-d5de-401d-bbb9-882b94f57811/thiago/Documents/UTS/sensors-and-control/assignments/fetch-robot-grasper/ros_ws/src/fetch_ros/fetch_navigation

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/media/thiago/138f6b25-d5de-401d-bbb9-882b94f57811/thiago/Documents/UTS/sensors-and-control/assignments/fetch-robot-grasper/ros_ws/install")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/media/thiago/138f6b25-d5de-401d-bbb9-882b94f57811/thiago/Documents/UTS/sensors-and-control/assignments/fetch-robot-grasper/ros_ws/build/fetch_ros/fetch_navigation/catkin_generated/installspace/fetch_navigation.pc")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/fetch_navigation/cmake" TYPE FILE FILES
    "/media/thiago/138f6b25-d5de-401d-bbb9-882b94f57811/thiago/Documents/UTS/sensors-and-control/assignments/fetch-robot-grasper/ros_ws/build/fetch_ros/fetch_navigation/catkin_generated/installspace/fetch_navigationConfig.cmake"
    "/media/thiago/138f6b25-d5de-401d-bbb9-882b94f57811/thiago/Documents/UTS/sensors-and-control/assignments/fetch-robot-grasper/ros_ws/build/fetch_ros/fetch_navigation/catkin_generated/installspace/fetch_navigationConfig-version.cmake"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/fetch_navigation" TYPE FILE FILES "/media/thiago/138f6b25-d5de-401d-bbb9-882b94f57811/thiago/Documents/UTS/sensors-and-control/assignments/fetch-robot-grasper/ros_ws/src/fetch_ros/fetch_navigation/package.xml")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/fetch_navigation" TYPE DIRECTORY FILES "/media/thiago/138f6b25-d5de-401d-bbb9-882b94f57811/thiago/Documents/UTS/sensors-and-control/assignments/fetch-robot-grasper/ros_ws/src/fetch_ros/fetch_navigation/config")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/fetch_navigation" TYPE DIRECTORY FILES "/media/thiago/138f6b25-d5de-401d-bbb9-882b94f57811/thiago/Documents/UTS/sensors-and-control/assignments/fetch-robot-grasper/ros_ws/src/fetch_ros/fetch_navigation/launch")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/fetch_navigation" TYPE PROGRAM FILES "/media/thiago/138f6b25-d5de-401d-bbb9-882b94f57811/thiago/Documents/UTS/sensors-and-control/assignments/fetch-robot-grasper/ros_ws/src/fetch_ros/fetch_navigation/scripts/tilt_head.py")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

