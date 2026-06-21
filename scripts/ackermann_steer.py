#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

MAX_STEER = 0.5   # radians
WHEELBASE = 0.45

class AckermannSteer:
    def __init__(self):
        rospy.init_node("ackermann_steer_node")

        self.sub = rospy.Subscriber("/cmd_vel", Twist, self.cmd_cb)
        self.set_state = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)

        self.speed = 0.0
        self.steer = 0.0

    def cmd_cb(self, msg):
        self.speed = msg.linear.x
        self.steer = max(min(msg.angular.z, MAX_STEER), -MAX_STEER)
        self.update()

    def update(self):
        state = ModelState()
        state.model_name = "ackermann_car"

        # Move forward
        state.twist.linear.x = self.speed
        state.twist.angular.z = self.steer

        try:
            self.set_state(state)
        except:
            pass

if __name__ == "__main__":
    rospy.wait_for_service("/gazebo/set_model_state")
    AckermannSteer()
    rospy.spin()
