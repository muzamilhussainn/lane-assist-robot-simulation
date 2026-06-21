#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point

# PID Gains
Kp = 0.004
Ki = 0.0000
Kd = 0.002

last_error = 0
integral = 0

def lane_callback(msg):
    global last_error, integral

    error = msg.x                         # lane offset in pixels
    integral += error
    derivative = error - last_error
    last_error = error

    # PID steering output
    steering = -(Kp * error + Ki * integral + Kd * derivative)

    # Create velocity command
    cmd = Twist()
    cmd.linear.x = 0.6    # forward speed
    cmd.angular.z = steering

    pub.publish(cmd)
    rospy.loginfo(f"error={error:.1f}, steer={steering:.3f}")

def start():
    rospy.init_node("lane_pid_controller")
    rospy.Subscriber("/lane/target_point", Point, lane_callback)

    global pub
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    rospy.loginfo("PID lane controller started.")
    rospy.spin()

if __name__ == "__main__":
    start()
