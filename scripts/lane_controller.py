#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Point, Twist

class LaneController:
    def __init__(self):
        # P-only control (NO PID)
        self.k_angular = rospy.get_param("~k_angular", 0.003)
        self.max_ang   = rospy.get_param("~max_ang", 0.7)
        self.speed     = rospy.get_param("~speed", 0.8)
        self.image_width = rospy.get_param("~image_width", 640)

        # Smoothing (low-pass filter). alpha 0.1–0.3 is typical.
        self.alpha = rospy.get_param("~alpha", 0.2)
        self.ang_prev = 0.0

        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.sub = rospy.Subscriber("/lane/target_point", Point, self.cb, queue_size=1)

        rospy.loginfo("Lane controller started (P-only + smoothing, no PID)")

    def cb(self, pt):
        error_px = pt.x - (self.image_width / 2.0)

        # P control
        ang = self.k_angular * error_px

        # Clamp
        if ang > self.max_ang:
            ang = self.max_ang
        elif ang < -self.max_ang:
            ang = -self.max_ang

        # Smooth (low-pass)
        ang = self.alpha * ang + (1.0 - self.alpha) * self.ang_prev
        self.ang_prev = ang

        cmd = Twist()
        cmd.linear.x = self.speed
        cmd.angular.z = ang
        self.cmd_pub.publish(cmd)

        rospy.loginfo_throttle(0.5, f"error_px={error_px:.1f} ang={ang:.3f} speed={self.speed:.2f}")

def main():
    rospy.init_node("lane_controller_node")
    LaneController()
    rospy.spin()

if __name__ == "__main__":
    main()

