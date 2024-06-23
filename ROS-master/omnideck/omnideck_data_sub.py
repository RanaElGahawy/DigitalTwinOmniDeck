#!/usr/bin/env python3
#get the odom data from the dashboard for the drone through "turtlebot_odom_namespace" namespace 
import rospy
import sys
from geometry_msgs.msg import Twist
import sys, select, os
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import socketio


sio = socketio.Client()



BURGER_MAX_LIN_VEL = 5.0
BURGER_MAX_ANG_VEL = 2.84

WAFFLE_MAX_LIN_VEL = 0.26
WAFFLE_MAX_ANG_VEL = 1.82

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1


def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel,target_angular_vel)

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    if turtlebot3_model == "burger":
      vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
    elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)
    else:
      vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)

    return vel

def checkAngularLimitVelocity(vel):
    if turtlebot3_model == "burger":
      vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
    elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)
    else:
      vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)

    return vel

@sio.on('turtlebot_omnideck_data',namespace='/turtlebot_omnideck')
def turtlebot_omnideck_data(data):
    global desired_orientation, desired_position
    #depending on the data needed by the drone, [the desired position and orientation, and then we need to publish to the appropriate topic]
    # Assuming the data received from socket.io contains the desired position and orientation.
    # desired_position = [data['position']['x'], data['position']['y'], data['position']['z']]
    # desired_orientation = [data['orientation']['x'], data['orientation']['y'], data['orientation']['z'], data['orientation']['w']]
    twist = Twist()
    twist.linear.x =checkLinearLimitVelocity(data['linear_velocity']['x'])
    twist.linear.y= checkLinearLimitVelocity(data['linear_velocity']['y'])
    twist.linear.z= checkLinearLimitVelocity(data['linear_velocity']['z'])
    twist.angular.x= checkAngularLimitVelocity(data['angular_velocity']['x'])
    twist.angular.y= checkAngularLimitVelocity(data['angular_velocity']['y'])
    twist.angular.z= checkAngularLimitVelocity(data['angular_velocity']['z'])
    pub.publish(twist)

#add anther function to get the rest of the coordinates 




if __name__ == '__main__':
    try:
        turtlebot3_model = rospy.get_param("model", "waffle_pi")
        rospy.init_node('aa')
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        # odom_sub = rospy.Subscriber('/odom', Odometry, odom_callback) # we are uncommenting this so that it mirrors the physical 
        sio.connect('http://192.168.105.194:8000', namespaces=['/turtlebot_omnideck_namespace'])  # added namespace here
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
