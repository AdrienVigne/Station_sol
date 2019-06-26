import numpy as np
import cv2

class Camera(object):
    """docstring for Camera."""

    def __init__(self, hote):
        super(Camera, self).__init__()
        self.hote = hote
        self.cap = None
        self.last_frame = np.zeros((1,1))

    def initialize(self):
        self.cap=cv2.VideoCapture(self.hote)

    def movie(self):
        self.last_frame = self.cap.read()
        #print(self.last_frame)

    def close_camera(self):
        self.cap.release()
