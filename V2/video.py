from PySide2.QtWidgets import QMainWindow,QWidget,QPushButton,QVBoxLayout,QApplication,QLabel,QHBoxLayout
from PySide2.QtCore import QThread,QTimer,Signal
from PySide2.QtGui import QImage,QPainter,QPixmap
from Client import Client
import pyqtgraph as pg
from Camera import Camera
import numpy as np

class camera_view(QWidget):
    """docstring for camera_view."""

    def __init__(self, camera):
        super(camera_view, self).__init__()
        self.camera = camera
        self.image_camera = np.zeros((1,1))
        #self.image = QImage()
        self.image2 = QLabel()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image2)
        #self.layout.addWidget(self.image)
        #self.addLayout(self.layout)
        self.setLayout(self.layout)
        

        #self.Timer.timeout.connect(self.setImage)
        #self.Timer.setInterval(200)
        self.movie_thread = MovieThread(self.camera)
        self.movie_thread.changePixmap.connect(self.setImage)
        self.movie_thread.start()
        #self.Timer.start()




    def setImage(self,image):
        self.image2.setPixmap(QPixmap.fromImage(image))



class MovieThread(QThread):
    changePixmap = Signal(QImage)

    def __init__(self, camera):
        super().__init__()
        self.camera = camera


    def run(self):
        while 1 :
            #print("thread")
            self.camera.movie()
            if self.camera.last_frame is not np.zeros((1,1)):
                #print("coucou")
                self.image_camera = self.camera.last_frame[1]
                #print(self.image_camera)
                #print(self.image_camera)
                height, width, channel = self.image_camera.shape
                bytesPerLine = 3* width
                self.image = QImage(self.image_camera.data,width,height,bytesPerLine, QImage.Format_RGB888).rgbSwapped()
                #print(self.image)
                #self.painter.drawImage(0,0,self.image)


                self.changePixmap.emit(self.image)





if __name__ == '__main__':
    app = QApplication([])
    C = Camera("http://192.168.1.41:8000/stream.mjpg")
    C.initialize()
    window = camera_view(C)
    window.show()
    app.exit(app.exec_())
