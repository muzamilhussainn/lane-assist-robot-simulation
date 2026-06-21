#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge

class LaneDetector:
    def __init__(self):
        self.bridge = CvBridge()

        self.sub = rospy.Subscriber("/camera/image_raw", Image, self.cb, queue_size=1)
        self.img_pub = rospy.Publisher("/lane/debug_image", Image, queue_size=1)
        self.point_pub = rospy.Publisher("/lane/target_point", Point, queue_size=1)

        rospy.loginfo("Lane detector with center started")

    def cb(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        h, w = frame.shape[:2]

        roi = frame[int(h*0.6):h, :]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        lines = cv2.HoughLinesP(
            edges, 1, np.pi/180,
            threshold=60, minLineLength=50, maxLineGap=50
        )

        left_x = []
        right_x = []

        if lines is not None:
            for l in lines:
                x1, y1, x2, y2 = l[0]
                if x1 < w / 2 and x2 < w / 2:
                    left_x.extend([x1, x2])
                elif x1 > w / 2 and x2 > w / 2:
                    right_x.extend([x1, x2])
                cv2.line(roi, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if left_x and right_x:
            left_lane = int(np.mean(left_x))
            right_lane = int(np.mean(right_x))
            center_x = int((left_lane + right_lane) / 2)

            y = roi.shape[0] - 10
            cv2.circle(roi, (center_x, y), 8, (0, 0, 255), -1)

            pt = Point()
            pt.x = center_x
            pt.y = y
            pt.z = 0.0
            self.point_pub.publish(pt)

        frame[int(h*0.6):h, :] = roi
        out = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        self.img_pub.publish(out)

def main():
    rospy.init_node("lane_detector_node")
    LaneDetector()
    rospy.spin()

if __name__ == "__main__":
    main()
