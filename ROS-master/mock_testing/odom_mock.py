#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Pose, Point, Twist, Vector3
import math

def publish_odometry():
    rospy.init_node('mock_odom_publisher')
    odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    odom = Odometry()
    odom.header.frame_id = "odom"
    odom.child_frame_id = "base_link"

    # Simulate some odometry data
    x = 0.0
    y = 0.0
    th = 0.0

    vx = 0.1  # linear velocity in x
    vy = 0.0  # linear velocity in y
    vth = 0.1  # angular velocity in theta

    current_time = rospy.Time.now()

    while not rospy.is_shutdown():
        current_time = rospy.Time.now()

        # Compute odometry in a typical way given the velocities of the robot
        dt = 1.0 / 10
        delta_x = vx * dt
        delta_y = vy * dt
        delta_th = vth * dt

        x += delta_x
        y += delta_y
        th += delta_th

        # Create quaternion from yaw
        odom_quat = Quaternion(*quaternion_from_euler(0, 0, th))

        # Update odometry message
        odom.header.stamp = current_time
        odom.pose.pose = Pose(Point(x, y, 0.0), odom_quat)
        odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth))

        # Publish odometry message
        odom_pub.publish(odom)

        rate.sleep()

def quaternion_from_euler(roll, pitch, yaw):
    """
    Convert an Euler angle to a quaternion.
    """
    q = Quaternion()
    t0 = math.cos(yaw * 0.5)
    t1 = math.sin(yaw * 0.5)
    t2 = math.cos(roll * 0.5)
    t3 = math.sin(roll * 0.5)
    t4 = math.cos(pitch * 0.5)
    t5 = math.sin(pitch * 0.5)

    q.w = t0 * t2 * t4 + t1 * t3 * t5
    q.x = t0 * t3 * t4 - t1 * t2 * t5
    q.y = t0 * t2 * t5 + t1 * t3 * t4
    q.z = t1 * t2 * t4 - t0 * t3 * t5

    return [q.x, q.y, q.z, q.w]

if __name__ == '__main__':
    try:
        publish_odometry()
    except rospy.ROSInterruptException:
        pass
