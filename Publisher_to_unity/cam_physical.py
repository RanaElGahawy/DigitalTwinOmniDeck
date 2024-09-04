
#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image, CompressedImage   # Import CompressedImage for efficient data transfer
from cv_bridge import CvBridge
import cv2
import socketio
import  base64

sio = socketio.Client()


def usb_camera_publisher():
    rospy.init_node('usb_camera_publisher', anonymous=True)
    image_pub = rospy.Publisher('/cam', CompressedImage, queue_size=10)  # Use CompressedImage for efficient data transfer
    bridge = CvBridge()

    cap = cv2.VideoCapture(1)  # 0 for the default camera

    if not cap.isOpened():
        rospy.logerr("Could not open USB camera.")
        return

    rospy.loginfo("USB camera opened successfully.")

    rate = rospy.Rate(30)  # Adjust frame rate as needed
    counter = 0
    while 1:
        ret, frame = cap.read()
        if ret:
            # Convert the frame to ROS CompressedImage message
            ros_compressed_image = CompressedImage()
            ros_compressed_image.header.stamp = rospy.Time.now()
            ros_compressed_image.format = "jpeg"  # Use JPEG format for compression

            # Resize the frame to 200x200 pixels
            resized_frame = cv2.resize(frame, (200, 200))
            # Encode the frame to JPEG format
            success, encoded_image = cv2.imencode('.jpg', resized_frame)
            if success:
                
                rospy.logwarn("publish image.")
                ros_compressed_image.data = encoded_image.tobytes()
                ros_compressed_image_base64 = base64.b64encode(ros_compressed_image.data).decode('utf-8')
                #image_pub.publish(ros_compressed_image)
                try:
                    sio.emit('cam_event', {'data': encoded_image.tobytes()}  ,namespace='/cam_namespace')
                except Exception as e:
                    print("An error occurred while emitting the event:", e)
                    #sio.connect('http://100.67.96.27:8000', namespaces=['/cam_namespace'])
                    sio.emit('cam_event', {'data': encoded_image}  ,namespace='/cam_namespace')
                    
                # else:
                #     rospy.logwarn("skip image.")
                
            else:
                rospy.logwarn("Failed to encode frame to JPEG.")
        else:
            rospy.logwarn("Failed to read frame from USB camera.")

        #rate.sleep()

    cap.release()

if __name__ == '__main__':
    try:
        #usb_camera_publisher()
        sio.connect('http://100.67.96.27:8000', namespaces=['/cam_namespace'])
        usb_camera_publisher()
        while not rospy.is_shutdown():
            rospy.sleep(1)
    except rospy.ROSInterruptException:
        pass
