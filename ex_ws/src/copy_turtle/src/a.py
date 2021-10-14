#!/usr/bin/python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import numpy as np

POSE = None
send = rospy.Publisher('/second/cmd_vel', Twist, queue_size=5)

def receive_pose_first(new_pose):
    if not POSE:
        return
    x = new_pose.x
    y = new_pose.y
    theta = np.arctan2((x - POSE[0]),(y - POSE[1]))
    twist = Twist()
    twist.angular.z = theta - POSE[2]
    twist.linear.x = x - POSE[0]
    twist.linear.y = y - POSE[1]
    send.publish(twist)

    
def receive_pose_second(new_pose):
    global POSE
    x = new_pose.x
    y = new_pose.y
    theta = new_pose.theta
    POSE = (x, y, theta)

first_pose_receiver = rospy.Subscriber('/turtle1/pose', Pose, receive_pose_first)
second_pose_receiver = rospy.Subscriber('/second/pose', Pose, receive_pose_second)
rospy.init_node('copy_turtle')
rospy.spin()
