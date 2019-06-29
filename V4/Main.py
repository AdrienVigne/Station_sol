import sys
from fenetre_graph import Fenetre_graph
from PySide2.QtWidgets import QApplication , QWidget, QVBoxLayout, QHBoxLayout
from PySide2.QtGui import QIcon
from PySide2.QtCore import QPoint,Qt

from Gps import Affichage_GPS
from video import camera_view
from Camera import Camera
from trajectoires import widget_trajectoire
from shell import shell

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)


#app.setWindowIcon(QIcon('/media/cnes-inisat/Donnees/Mega/python/Client/inisat.jpg'))
fen1 = Fenetre_graph("192.168.1.6",31000,56880)
fen1.setWindowTitle('Télémétrie')
#fen1.move(QPoint(1080,0))

#fen1.setWindowIcon(QIcon('inisat.png'))

fen1.showMaximized()

Cam = Camera("http://192.168.1.45:8000/stream.mjpg")
Cam.initialize()

GPS = Affichage_GPS(fen1,fen1.Timer)
box_fen2  = QHBoxLayout()
box_fen2.addWidget(GPS)
box_fen2.addWidget(camera_view(Cam))
box2=QVBoxLayout()
box2.addLayout(box_fen2)
box2.addWidget(shell(fen1))
fen2 = QWidget()

p = fen2.palette()
fen2.setAutoFillBackground(True)
p.setColor(fen2.backgroundRole(),Qt.darkGray)
fen2.setPalette(p)

fen2.setLayout(box2)
fen2.setWindowTitle('GPS_Vidéo_Shell')
fen2.show()



fen3 = QWidget()
box = QVBoxLayout()

box.addWidget(widget_trajectoire())
fen3.setWindowTitle("Controle Drone")
fen3.setLayout(box)
fen3.show()



app.exec_()
