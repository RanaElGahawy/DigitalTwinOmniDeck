#!/usr/bin/env python3

##### Description 
#recieves the omnideck and the VR headset data through socketio and publishes them to move the drone
import rospy
from geometry_msgs.msg import Twist
import socketio
import time


sio = socketio.Client()

prev_position = None
prev_time = None 

def calculate_velocities(current_position, prev_position, dt):
    if prev_position is None or dt == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0
    
    dx = current_position['x'] - prev_position['x']
    dy = current_position['y'] - prev_position['y']
    dtheta_x = current_position['orientation_x'] - prev_position['orientation_x']
    dtheta_y = current_position['orientation_y'] - prev_position['orientation_y']
    dtheta_z = current_position['orientation_z'] - prev_position['orientation_z']
    
    
    linear_velocity_x = dx / dt
    linear_velocity_y = dy / dt
    
    angular_velocity_x = dtheta_x / dt
    angular_velocity_y = dtheta_y / dt
    angular_velocity_z = dtheta_z / dt
    
    return linear_velocity_x, linear_velocity_y, angular_velocity_x, angular_velocity_y, angular_velocity_z
       
@sio.on('omnideck_data',namespace='/omnideck')
def omnideck_data(data):
    global prev_position, prev_time
    
    current_time = time.time()
    if prev_time is None:
        dt = 0
    else:
        dt = current_time - prev_time
    
    current_position = {
        'x': data['position']['x'],
        'y': data['position']['y'],
        'orientation_x': data['orientation']['x'],
        'orientation_y': data['orientation']['y'],
        'orientation_z': data['orientation']['z']
    }
    
    linear_velocity_x, linear_velocity_y, angular_velocity_x, angular_velocity_y, angular_velocity_z = calculate_velocities(current_position, prev_position, dt)
    
    twist = Twist()
    twist.linear.x = linear_velocity_x
    twist.linear.y = linear_velocity_y
    twist.angular.x = angular_velocity_x
    twist.angular.y = angular_velocity_y
    twist.angular.z = angular_velocity_z
    
    pub.publish(twist)
    
    prev_position = current_position
    prev_time = current_time



#add anther function to receive data from the VR headset and calculate the height.
# edit the topic according to those of the drone




if __name__ == '__main__':
    try:
        rospy.init_node('drone_controller')
        sio.connect('http://192.168.202.6:8000', namespaces=['/omnideck_data_namespace'])  
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
