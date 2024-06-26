#!/usr/bin/env python3

#subscribe to the odom data from the turtlebot and sending it over dashboard on the "turtlebot_odom_namespace" namespace 

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import socketio

sio = socketio.Client()

def odom_callback(odom_data):

    # Extract linear and angular velocities from the odom topic
    linear_velocity = odom_data.twist.twist.linear
    angular_velocity = odom_data.twist.twist.angular

    # Convert the Odometry data to a dictionary
    odom_dict = {
        'position': {
            'x': odom_data.pose.pose.position.x,
            'y': odom_data.pose.pose.position.y,
            #'z': odom_data.pose.pose.position.z
        },
        'orientation': {
            'x': odom_data.pose.pose.orientation.x,
            'y': odom_data.pose.pose.orientation.y,
            #'z': odom_data.pose.pose.orientation.z,
            #'w': odom_data.pose.pose.orientation.w
        },
        'linear_velocity': {
            'x': linear_velocity.x,
            'y': linear_velocity.y,
           # 'z': linear_velocity.z
        },
        'angular_velocity': {
            'x': angular_velocity.x,
            'y': angular_velocity.y,
            #    'z': angular_velocity.z
        }
    }
    
    # Send the odometry data to the Socket.io server
    sio.emit('turtlebot_odom_event', odom_dict, namespace='/turtlebot_odom_namespace')
    print("sent to digital")


if __name__ == '__main__':
    try:
        turtlebot3_model = rospy.get_param("model", "waffle_pi")
        rospy.init_node('aa')
        odom_sub = rospy.Subscriber('/odom', Odometry, odom_callback) 
        sio.connect('http://192.168.105.194:8000', namespaces=['/turtlebot_odom_namespace'])  # added namespace here
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
