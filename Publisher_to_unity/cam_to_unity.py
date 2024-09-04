import rospy
from sensor_msgs.msg import  CompressedImage  
import socketio
import base64


sio = socketio.Client()

rospy.init_node('camera_feed_to_unity', anonymous=True)
pub = rospy.Publisher('/cam', CompressedImage, queue_size=10)



@sio.on('cam_callback',namespace='/camera_feed')

def cam_callback(data):

    received_base64_data = data['data']
    print(received_base64_data)
    # image_data = base64.b64decode(received_base64_data)
    
    # # Create a CompressedImage message
    # compressed_img_msg = CompressedImage()
    # compressed_img_msg.header.stamp = rospy.Time.now()  # Add a timestamp
    # compressed_img_msg.format = "jpeg"  # Set the compression format
    # compressed_img_msg.data = image_data  # Set the image data
    # print("publishing pics")
    # # Publish the CompressedImage message
    # pub.publish(compressed_img_msg)
        

sio.connect('http://100.67.96.27:8000', namespaces=['/camera_feed'])
rospy.spin() 
