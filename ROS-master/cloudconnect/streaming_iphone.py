import sys, os
import cv2
import numpy as np
import socketio
import base64
import time
import threading

from gtts import gTTS
from playsound import playsound

class CVClient(object):
    def __init__(self, server_addr, stream_fps):
        self.server_addr = server_addr
        self.server_port = 8000
        self._stream_fps = stream_fps
        self._last_update_t = time.time()
        self._wait_t = (1/self._stream_fps)

    def _convert_image_to_jpeg(self, image):
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)

    def send_data(self, frame):
        cur_t = time.time()
        if cur_t - self._last_update_t > self._wait_t:
            self._last_update_t = cur_t
            sio.emit(
                'cv2serverphysical',
                {
                    'image': self._convert_image_to_jpeg(frame),
                }, namespace='/cv'
            )

    def close(self):
        sio.disconnect()


def image_callback():
    print("Received an image!")
    try:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                break
            frame = cv2.resize(frame, (300, 150), interpolation=cv2.INTER_AREA)
            streamer.send_data(frame)
    except Exception as e:
        print("Error in image_callback:", str(e))
    finally:
        cap.release()


sio = socketio.Client()


@sio.event(namespace='/cv')
def connect():
    global streamer
    streamer = CVClient('localhost', 5.0)
    print('[INFO] Successfully connected to server.')
    # Start image capturing in a new thread to avoid blocking
    image_thread = threading.Thread(target=image_callback)
    image_thread.start()
    return image_thread


@sio.event(namespace='/cv')
def connect_error():
    print('[INFO] Failed to connect to server.')


@sio.event(namespace='/cv')
def disconnect():
    print('[INFO] Disconnected from server.')


@sio.on('omnideck_data', namespace='/omnideck')

def omnideck_data(data):
   # print("received "+ str(data))
    text = "move" + data
    tts = gTTS(text)
    tts.save("speech.mp3")
    playsound("speech.mp3")
    os.remove("speech.mp3")

if __name__ == '__main__':
    # Establish the connection
    sio.connect('http://localhost:8000', namespaces=['/omnideck', '/cv' ])
    image_thread = connect()  
    image_thread.join()
    streamer.close()
