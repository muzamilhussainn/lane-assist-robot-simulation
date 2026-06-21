# Project Summary

This project implements a ROS-based lane assist system for a simulated ground vehicle in Gazebo. A front-facing camera publishes road images, OpenCV is used to detect lane markings, and a proportional controller converts the lane offset into steering commands. The system was tested on straight and curved road segments in simulation.

## Main ROS Nodes

- `lane_detector.py`: subscribes to `/camera/image_raw`, processes the image, and publishes the lane target point on `/lane/target_point`.
- `lane_controller.py`: subscribes to `/lane/target_point` and publishes velocity commands on `/cmd_vel`.
- `ackermann_bridge.py`: converts `/cmd_vel` commands into steering and rear wheel commands for the simulated vehicle.

## Topics

- `/camera/image_raw`
- `/lane/debug_image`
- `/lane/target_point`
- `/cmd_vel`

## Tools Used

ROS Noetic, Gazebo, Python, OpenCV, cv_bridge, geometry_msgs, sensor_msgs, std_msgs.
