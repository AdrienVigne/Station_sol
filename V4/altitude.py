from PySide2.QtWidgets import QMainWindow,QWidget,QPushButton,QVBoxLayout,QApplication,QLabel,QHBoxLayout
from PySide2.QtCore import QThread,QTimer,Qt
from PySide2.QtGui import QPen,QColor
from Client import Client
import pyqtgraph as pg
from donnees import traitement
from time import sleep

#recu = None

class altitude(QWidget):

    def __init__(self,fenetre_graph):
        super().__init__()

            
        self.Donnees = traitement()

        p = self.palette()
        self.setAutoFillBackground(True)
        p.setColor(self.backgroundRole(),Qt.black)
        self.setPalette(p)

        self.graphAcc = pg.PlotWidget()
        self.Legend_Acc = self.graphAcc.addLegend()
        self.taille_Acc_x = 100
        #self.graphAcc.setXRange(0, 200,padding = 0)

        self.graphGyro = pg.PlotWidget()
        self.Legend_Gyro = self.graphGyro.addLegend()
        self.taille_Gyro_x = 100

        self.graphMagneto = pg.PlotWidget()
        self.Legend_Magneto = self.graphMagneto.addLegend()
        self.taille_Magneto_x = 100
