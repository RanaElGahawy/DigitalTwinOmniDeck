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
def omnideck_callback(odom_data):
    omnideck_pos_x, omnideck_pos_y, omnideck_pos_z, omnideck_orient_x, omnnideck_orient_y, omnnideck_orient_z, omnideck_orient_w, omnideck_lin_vel_x,\
    omnideck_lin_vel_y, omnideck_lin_vel_z, omnideck_ang_vel_x, omnideck_ang_vel_y, omnideck_ang_vel_z = odom_data.split(',')
    odom_dict = {
        'position': {
            'x': omnideck_pos_x,
            'y': omnideck_pos_y,
            'z': omnideck_pos_z
        },
        'orientation': {
            'x': omnideck_orient_x,
            'y': omnnideck_orient_y,
            'z': omnnideck_orient_z,
            'w': omnideck_orient_w
        },
        'linear_velocity': {
            'x': omnideck_lin_vel_x,
            'y': omnideck_lin_vel_y,
            'z': omnideck_lin_vel_z
        },
        'angular_velocity': {
            'x': omnideck_ang_vel_x,
            'y': omnideck_ang_vel_y,
            'z': omnideck_ang_vel_z 
        }
    }
    # Send the odometry data to the Socket.io server
    sio.emit('turtlebot_omnideck_event', odom_dict, namespace='/turtlebot_omnideck_namespace')
    print("sent to digital")


if __name__ == '__main__':
    try:
        turtlebot3_model = rospy.get_param("model", "waffle_pi")
        rospy.init_node('aa')
        odom_sub = rospy.Subscriber('/omnideck_data', String, omnideck_callback) # we are uncommenting this so that it mirrors the physical 
        sio.connect('http://192.168.105.194:8000', namespaces=['/turtlebot_omnideck_namespace'])  # added namespace here
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
