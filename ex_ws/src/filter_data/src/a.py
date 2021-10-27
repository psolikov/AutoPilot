#!/usr/bin/python3

import rospy
from sensor_msgs.msg import LaserScan

publisher = rospy.Publisher('/no-outliers', LaserScan, queue_size=5)

def filter(message):
    m_size = len(message.ranges)
    remove = []
    N = 4
    for i in range(m_size):
        neighbours_idx = []
        for j in range(N // 2):
            if i - j > 0:
                neighbours_idx.append(i - j)
            if i + j < m_size:
                neighbours_idx.append(i + j)
        neighbours = [message.ranges[idx] for idx in neighbours_idx]
        sum_delta = 0
        for j in range(1, len(neighbours)):
            sum_delta += abs(neighbours[j] - neighbours[j - 1])
        if sum_delta > 0.1:
            remove += neighbours_idx
    remove = set(remove)
    message.ranges = [point for (idx, point) in enumerate (message.ranges) if idx not in remove]
    publisher.publish(message)

subscriber = rospy.Subscriber('/base_scan', LaserScan, filter)

rospy.init_node('no-outliers-node')
rospy.spin()