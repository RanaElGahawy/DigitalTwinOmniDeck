#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Twist
import sys, select, os
from gazebo_msgs.srv import SetModelState
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import socketio



sio = socketio.Client()
global desired_position, desired_orientation, model_name


# @sio.event(namespace='/movement')
# def actuateData(data):
#     print(data)p
#     move(data)
GAZEBO_API_URL= "http://$HOST_IP:11346"

# @sio.event(namespace='/dummy_namespace')
# def connect():
#     print('[INFO] Successfully connected to server.')

def set_model_state(msg):
    rospy.wait_for_service('/gazebo/set_model_state')
    
    try:
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

        state_msg = ModelState()
        # state_msg.model_name = 'turtlebot3'
        # print('X: ')
        # print(msg['position']['x'])
        # state_msg.pose.position.x = msg['position']['x']
        # state_msg.pose.position.y = msg['position']['y']
        # state_msg.pose.position.z = msg['position']['z']
        # state_msg.pose.orientation.x = msg['orientation']['x']
        # state_msg.pose.orientation.y = msg['orientation']['y']
        # state_msg.pose.orientation.z = msg['orientation']['z']
        # state_msg.pose.orientation.w = msg['orientation']['w']

        state_msg.twist.linear.x = msg['linear_velocity']['x']
        state_msg.twist.linear.y = msg['linear_velocity']['y']
        state_msg.twist.linear.z = msg['linear_velocity']['z']

        state_msg.twist.angular.x = msg['angular_velocity']['x']
        state_msg.twist.angular.y = msg['angular_velocity']['y']
        state_msg.twist.angular.z = msg['angular_velocity']['z']
        state_msg.pose.position.x = msg.pose.pose.position.x + 0.001
        state_msg.pose.position.y = msg.pose.pose.position.y
        state_msg.pose.position.z = msg.pose.pose.position.z
        state_msg.pose.orientation.x = msg.pose.pose.orientation.x + 0.01
        state_msg.pose.orientation.y = msg.pose.pose.orientation.y
        state_msg.pose.orientation.z = msg.pose.pose.orientation.z
        state_msg.pose.orientation.w = msg.pose.pose.orientation.w

        response = set_state(state_msg)

        if response.success:
            rospy.loginfo(f"Successfully set state for {state_msg.model_name}")
        else:
            rospy.logerr(f"Failed to set state for {state_msg.model_name}: {response.status_message}")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")

        
@sio.on('gazeboData',namespace='/manga')
def gazeboData(data):
    global desired_orientation, desired_position, model_name
    print("HI!!")
    #print(odom_dict)
    # Assuming the data received from socket.io contains the desired position and orientation.
    # desired_position = [data['position']['x'], data['position']['y'], data['position']['z']]
    # desired_orientation = [data['orientation']['x'], data['orientation']['y'], data['orientation']['z'], data['orientation']['w']]
    # model_name = 'turtlebot3'
    set_model_state(data)


   # print(data)

if __name__ == '__main__':
    rospy.init_node('gazebo_asset_control')

    sio.connect('http://0.0.0.0:8000',namespaces=[ '/manga'])

    # Specify the model name and desired pose
    

    # Set the model state

    # sub = rospy.Subscriber('/odom',Odometry,set_model_state)
    # set_model_state(model_name, desired_position, desired_orientation)

    # Spin to keep the script alive
    # sio.connect(GAZEBO_API_URL)
    rospy.spin()
