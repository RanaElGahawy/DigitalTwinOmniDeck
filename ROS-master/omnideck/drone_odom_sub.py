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
       
@sio.on('turtlebot_odom_data',namespace='/turtlebot_odom')
def turtlebot_odom_data(data):
    global desired_orientation, desired_position
    #depending on the data needed by the drone, [the desired position and orientation, and then we need to publish to the appropriate topic]
    # Assuming the data received from socket.io contains the desired position and orientation.
    desired_position = [data['position']['x'], data['position']['y'], data['position']['z']]
    desired_orientation = [data['orientation']['x'], data['orientation']['y'], data['orientation']['z'], data['orientation']['w']]


#add anther function to get the rest of the coordinates 




if __name__ == '__main__':
    try:
        turtlebot3_model = rospy.get_param("model", "waffle_pi")
        rospy.init_node('aa')
        # odom_sub = rospy.Subscriber('/odom', Odometry, odom_callback) # we are uncommenting this so that it mirrors the physical 
        sio.connect('http://192.168.105.194:8000', namespaces=['/turtlebot_odom_namespace'])  # added namespace here
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
