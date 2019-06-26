import sys
from fenetre_graph import Fenetre_graph
from PySide2.QtWidgets import QApplication , QWidget, QVBoxLayout, QHBoxLayout
from PySide2.QtGui import QIcon
from PySide2.QtCore import QPoint

from Gps import Affichage_GPS
from video import camera_view
from Camera import Camera
from trajectoires import widget_trajectoire


app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)


#app.setWindowIcon(QIcon('/media/cnes-inisat/Donnees/Mega/python/Client/inisat.jpg'))
fen1 = Fenetre_graph("192.168.1.70",31000)
fen1.setWindowTitle('Télémétrie')
#fen1.move(QPoint(1080,0))

#fen1.setWindowIcon(QIcon('inisat.png'))

fen1.showMaximized()


GPS = Affichage_GPS(fen1,fen1.Timer)
box_fen2  = QHBoxLayout()
box_fen2.addWidget(GPS)
box_fen2.addWidget(widget_trajectoire())
fen2 = QWidget()
fen2.setLayout(box_fen2)
fen2.setWindowTitle('GPS')
fen2.show()
Cam = Camera("http://192.168.1.62:8000/stream.mjpg")
Cam.initialize()


fen3 = QWidget()
box = QVBoxLayout()
box.addWidget(camera_view(Cam))

fen3.setLayout(box)
fen3.show()

app.exec_()
