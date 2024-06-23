#!/usr/bin/env python3
#subscribe to the odom data from the turtlebot and sending it over dashboard on the "turtlebot_odom_namespace" namespace 
import rospy
import sys
from geometry_msgs.msg import Twist
import sys, select, os
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import socketio
###
from std_msgs.msg import Bool
from datetime import datetime

###
from std_msgs.msg import Bool
from datetime import datetime

#from AUC-Thesis-DT-Physical/RemoteDrivingDashboard-master/apps/home/views.py import sio

sio = socketio.Client()


BURGER_MAX_LIN_VEL = 5.0
BURGER_MAX_ANG_VEL = 2.84

WAFFLE_MAX_LIN_VEL = 0.26
WAFFLE_MAX_ANG_VEL = 1.82

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1


# if __name__=="__main__": 

status = 0
target_linear_vel   = 0.0
target_angular_vel  = 0.0
control_linear_vel  = 0.0
control_angular_vel = 0.0



####### socket io to receive interrupt state 
def odom_callback(odom_data):

    global target_linear_vel , target_angular_vel
    # Extract linear and angular velocities from the odom topic
    linear_velocity = odom_data.twist.twist.linear
    angular_velocity = odom_data.twist.twist.angular
    # Convert the Odometry data to a dictionary
    odom_dict = {
        'position': {
            'x': odom_data.pose.pose.position.x,
            'y': odom_data.pose.pose.position.y,
            'z': odom_data.pose.pose.position.z
        },
        'orientation': {
            'x': odom_data.pose.pose.orientation.x,
            'y': odom_data.pose.pose.orientation.y,
            'z': odom_data.pose.pose.orientation.z,
            'w': odom_data.pose.pose.orientation.w
        },
        'linear_velocity': {
            'x': linear_velocity.x,
            'y': linear_velocity.y,
            'z': linear_velocity.z
        },
        'angular_velocity': {
            'x': angular_velocity.x,
            'y': angular_velocity.y,
            'z': angular_velocity.z
        }
    }
    # Send the odometry data to the Socket.io server
    sio.emit('turtlebot_odom_event', odom_dict, namespace='/turtlebot_odom_namespace')
    print("sent to digital")


if __name__ == '__main__':
    try:
        turtlebot3_model = rospy.get_param("model", "waffle_pi")
        rospy.init_node('aa')
        odom_sub = rospy.Subscriber('/odom', Odometry, odom_callback) # we are uncommenting this so that it mirrors the physical 
        sio.connect('http://192.168.105.194:8000', namespaces=['/turtlebot_odom_namespace'])  # added namespace here
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
