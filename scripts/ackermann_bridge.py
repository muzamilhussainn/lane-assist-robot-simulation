#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

class AckermannBridge:
    def __init__(self):
        rospy.init_node("ackermann_bridge")

        # Topics for joint controllers (we’ll create them in the SDF via gazebo plugins)
        self.pub_steer_left  = rospy.Publisher("/ackermann/steer_left/command", Float64, queue_size=1)
        self.pub_steer_right = rospy.Publisher("/ackermann/steer_right/command", Float64, queue_size=1)
        self.pub_rear_left   = rospy.Publisher("/ackermann/rear_left_wheel/command", Float64, queue_size=1)
        self.pub_rear_right  = rospy.Publisher("/ackermann/rear_right_wheel/command", Float64, queue_size=1)

        self.max_steer = rospy.get_param("~max_steer", 0.5)          # radians
        self.max_speed = rospy.get_param("~max_speed", 6.0)          # wheel angular speed rad/s
        self.speed_gain = rospy.get_param("~speed_gain", 8.0)        # converts linear.x to wheel rad/s

        rospy.Subscriber("/cmd_vel", Twist, self.cb)
        rospy.loginfo("Ackermann bridge started (no ros_control, no PID).")
        rospy.spin()

    def cb(self, msg: Twist):
        steer = msg.angular.z
        steer = max(min(steer, self.max_steer), -self.max_steer)

        # Convert forward speed to wheel angular speed (simple)
        wheel_speed = msg.linear.x * self.speed_gain
        wheel_speed = max(min(wheel_speed, self.max_speed), -self.max_speed)

        self.pub_steer_left.publish(Float64(steer))
        self.pub_steer_right.publish(Float64(steer))
        self.pub_rear_left.publish(Float64(wheel_speed))
        self.pub_rear_right.publish(Float64(wheel_speed))

if __name__ == "__main__":
    AckermannBridge()
