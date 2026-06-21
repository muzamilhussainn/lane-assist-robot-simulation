#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image

def image_callback(msg):
    rospy.loginfo("Camera image received")

def main():
    rospy.init_node('camera_test_node')
    
    rospy.Subscriber('/camera/image_raw', Image, image_callback)
    
    rospy.loginfo("Camera test node started")
    rospy.spin()

if __name__ == '__main__':
    main()
