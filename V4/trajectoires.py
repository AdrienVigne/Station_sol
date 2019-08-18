from PySide2.QtWidgets import QMainWindow,QWidget,QPushButton,QVBoxLayout,QApplication,QLabel,QHBoxLayout,QLineEdit
import pyqtgraph as pg
from pyqtgraph.widgets import MatplotlibWidget as mw
from numpy import *
from mpl_toolkits.mplot3d import axes3d, Axes3D
import csv
from ftplib import FTP
from Client import Client
import controle_drone

class widget_trajectoire(QWidget):
    """docstring for widget_trajectoire."""

    def __init__(self):
        super(widget_trajectoire, self).__init__()

        self.client = Client("192.168.1.70",35170)

        self.angle_aller = 0
        self.angle_retour = 0
        self.rayon = 10
        self.theta = linspace(0,pi,200)

        self.graph = mw.MatplotlibWidget()
        self.plot = self.graph.getFigure()
        self.axe = Axes3D(self.plot)
        self.axe.set_xlabel("x")
        self.axe.set_ylabel("y")
        self.axe.set_zlabel("z")


        #self.legend = self.graph.addLegend()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.graph)
        self.box1 = QHBoxLayout()
        #self.box1.addStretch(1)
        self.box_aller = QVBoxLayout()
        self.box_aller.addStretch(1)
        self.box_retour = QVBoxLayout()
        self.box_retour.addStretch(1)

        self.box1.addLayout(self.box_aller)
        self.box1.addLayout(self.box_retour)

        self.box2 =QHBoxLayout()
        #self.box2.addStretch(1)
        self.layout.addLayout(self.box1)
        self.layout.addLayout(self.box2)

        self.text_aller = QLabel("Paramètres de la trajectoire d'aller")
        self.text_angle_aller = QLabel("Angle : ")
        self.angle_aller_zone = QLineEdit()

        self.text_angle_retour = QLabel("Angle : ")
        self.angle_retour_zone = QLineEdit()

        self.text_rayon = QLabel("Rayon : ")
        self.rayon_zone = QLineEdit()
        self.text_retour = QLabel("Paramètres de la trajectoire de retour")

        self.box_angle_aller = QHBoxLayout()
        self.box_rayon = QHBoxLayout()
        self.box_angle_retour = QHBoxLayout()

        self.box_angle_aller.addWidget(self.text_angle_aller)
        self.box_angle_aller.addWidget(self.angle_aller_zone)

        self.box_angle_retour.addWidget(self.text_angle_retour)
        self.box_angle_retour.addWidget(self.angle_retour_zone)

        self.box_rayon.addWidget(self.text_rayon)
        self.box_rayon.addWidget(self.rayon_zone)

        self.box_aller.addWidget(self.text_aller)
        self.box_aller.addLayout(self.box_angle_aller)
        self.box_aller.addLayout(self.box_rayon)
        self.box_retour.addWidget(self.text_retour)
        self.box_retour.addLayout(self.box_angle_retour)
        self.boutton_tracer = QPushButton("Tracer")
        self.boutton_enregistrer = QPushButton("Enregistrer")
        self.boutton_transferer = QPushButton("Transferer")
        self.boutton_mouvement = QPushButton("Mouvement")
        self.box2.addWidget(self.boutton_tracer)
        self.box2.addWidget(self.boutton_enregistrer)
        self.box2.addWidget(self.boutton_transferer)
        self.box2.addWidget(self.boutton_mouvement)
        self.boutton_tracer.clicked.connect(self.Tracer)
        self.boutton_enregistrer.clicked.connect(self.Enregistrer)
        self.boutton_transferer.clicked.connect(self.Transferer)
        self.boutton_mouvement.clicked.connect(self.Mouvement)

        self.x = None
        self.y = None
        self.z = None

    def Tracer(self):
        #print(self.angle_aller_zone.text())
        if (self.angle_aller_zone.text() != ""):
            self.axe.clear()
            self.angle_aller = float(self.angle_aller_zone.text())
            self.rayon = float(self.rayon_zone.text())
            self.x = self.rayon * cos(self.theta)
            self.y = self.rayon * sin(self.theta) * sin((self.angle_aller/180)*pi)
            self.z = self.rayon * sin(self.theta) * cos((self.angle_aller/180)*pi)
            self.axe.plot(self.x,self.y,self.z)
            print(self.x,self.y,self.z)

            self.axe.legend()
            self.graph.draw()
            #print(self.angle_aller)
            #print(self.rayon)
    def Enregistrer(self):
        self.csv = vstack((self.x,self.y))
        #print(self.csv)
        self.csv = vstack((self.csv,self.z))
        #print(self.csv)
        savetxt("trajectoire.csv",self.csv.T,delimiter=";")
            #writer.writerows(self.y)
            #writer.writerows(self.z)

        pass
    def Transferer(self):
        #controle_drone.transfert()
        self.ftp = FTP("192.168.1.70","micro","python")
        self.ftp.sendcmd("CWD flash")
        f = open("trajectoire.csv",'rb')
        self.ftp.storbinary('STOR trajectoire.csv',f)
        f.close()
        self.ftp.quit()

    def Mouvement(self):
        self.client.envoie("255\r\n")





if __name__ == '__main__':
    app = QApplication([])
    window = widget_trajectoire()
    window.show()
    app.exit(app.exec_())
