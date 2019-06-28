from PySide2.QtWidgets import QMainWindow,QWidget,QPushButton,QVBoxLayout,QApplication,QLabel,QHBoxLayout,QToolButton
from PySide2.QtCore import QThread,QTimer,Signal,Qt
from PySide2.QtGui import QImage,QPainter,QPixmap
from Client import Client
import pyqtgraph as pg
from Camera import Camera
import numpy as np
from Client import Client

class camera_view(QWidget):
    """docstring for camera_view."""

    def __init__(self, camera):
        super(camera_view, self).__init__()
        self.camera = camera
        self.image_camera = np.zeros((1,1))
        #self.image = QImage()

        self.button_up = QToolButton()
        self.button_up.setArrowType(Qt.UpArrow)
        self.button_down = QToolButton()
        self.button_down.setArrowType(Qt.DownArrow)
        self.button_left = QToolButton()
        self.button_left.setArrowType(Qt.LeftArrow)
        self.button_right = QToolButton()
        self.button_right.setArrowType(Qt.RightArrow)

        self.box_button = QVBoxLayout()
        self.box_button_centre = QHBoxLayout()
        self.box_button_centre.addWidget(self.button_left)
        self.box_button_centre.addWidget(self.button_right)
        self.box_button_centre.addStretch(1)
        self.box_button.addWidget(self.button_up)
        self.box_button.addLayout(self.box_button_centre)
        self.box_button.addWidget(self.button_down)
        self.box_button.addStretch(1)

        self.button_affichage = QPushButton("Affichage Vidéo")
        self.button_affichage.clicked.connect(self.Affichage)

        self.button_stop = QPushButton("Stop retour Vidéo")
        self.button_stop.clicked.connect(self.fin_video)
        self.box = QVBoxLayout()
        self.box.addWidget(self.button_affichage)
        self.box.addWidget(self.button_stop)

        self.box_panel = QHBoxLayout()
        self.box_panel.addLayout(self.box)
        self.box_panel.addLayout(self.box_button)

        self.image2 = QLabel()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image2)

        self.layout.addLayout(self.box_panel)
        self.setLayout(self.layout)


        self.movie_thread = MovieThread(self.camera)
        self.movie_thread.changePixmap.connect(self.setImage)
        self.movie_thread.setTerminationEnabled(True)

        #
        self.button_up.clicked.connect(self.up)
        self.button_down.clicked.connect(self.down)
        self.button_right.clicked.connect(self.right)
        self.button_left.clicked.connect(self.left)

        #box enregistrement + photo
        self.button_debut_video = QPushButton("Début enregistrement Vidéo")
        self.button_fin_video = QPushButton("Fin enregistrement Vidéo")
        self.button_photo = QPushButton("Photo")
        self.box_video_photo = QVBoxLayout()
        self.box_video_photo.addWidget(self.button_debut_video)
        self.box_video_photo.addWidget(self.button_fin_video)
        self.box_video_photo.addWidget(self.button_photo)
        self.box_panel.addLayout(self.box_video_photo)





    def photo(self):

        pass

    def video_debut(self):

        pass


    def video_fin(self):

        pass



    def up(self):
        self.client.envoie('up')
        print('up')
        pass

    def down(self):
        self.client.envoie('down')
        print('down')

        pass

    def right(self):
        self.client.envoie('right')
        print('right')
        pass

    def left(self):
        self.client.envoie('left')
        print('left')
        pass

    def Affichage(self):
        self.client = Client("192.168.1.62",35351)

        self.movie_thread.start()

    def fin_video(self):
        self.movie_thread.stop()
        self.client.envoie('q')

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
    def stop(self):
        #print("coucou")
        self.terminate()





if __name__ == '__main__':
    app = QApplication([])
    C = Camera("http://192.168.1.62:8000/stream.mjpg")
    C.initialize()
    window = camera_view(C)
    window.show()
    app.exit(app.exec_())
