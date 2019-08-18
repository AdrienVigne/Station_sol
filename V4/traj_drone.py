from PySide2.QtWidgets import QMainWindow,QWidget,QPushButton,QVBoxLayout,QApplication,QLabel,QHBoxLayout
from PySide2.QtCore import QThread,QTimer,Qt
from PySide2.QtGui import QPen,QColor
from Client import Client
import pyqtgraph as pg
from pyqtgraph.widgets import MatplotlibWidget as mw
import tilemapbase
import numpy as np

from time import sleep

#recu = None

class traj_drone (QWidget):

    def __init__(self,fen1,fen_traj):
        super().__init__()
        #recupération des autres fenetre nécessaire
        self.fenetre_graph = fen1
        self.fen_traj = fen_traj


        #position de l'antenne utilisé comme centre du repère
        self.position_antenne = None
        #position en x,y,z dans le repère mathématiques
        self.X_traj = None
        self.Y_traj = None
        self.Z_traj = None
        #position en Latitude,Longitude,Altitude
        self.Latitude = None
        self.Longitude = None
        self.Altitude = None


        #creation de la base de données pour la carte
        tilemapbase.init(create=True)
        #creation de l'objet carte (lib MatplotlibWidget)
        self.graph = mw.MatplotlibWidget(size=(2,2),dpi=300)
        self.plot = self.graph.getFigure()
        self.graph.resize(800,800)
        self.axe = self.plot.add_subplot(111)
        self.axe.axis("off")

        #init et lancement du thread de mise a jour de la position_antenne
        self.thread_centre = thread_position_antenne(self.fenetre_graph)
        self.thread_centre.start()
        #init et lancement du thread de tracé gps
        self.thread_gps = thread_trace_gps(self.axe,self.graph)
        self.thread_gps.start()

        self.fen_traj.boutton_tracer.clicked.connect(self.tracer)
        self.fenetre_graph.Timer.timeout.connect(self.position_antenne_update)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.graph)
        self.setLayout(self.Vbox)

    def tracer(self):
        print("debut trace")
        self.X_traj = self.fen_traj.x
        self.Y_traj = self.fen_traj.y
        self.Z_traj = self.fen_traj.z
        print('x,y,z : ',self.X_traj,self.Y_traj,self.Z_traj)
        if self.position_antenne is not None :
            self.Longitude,self.Latitude = self.conversion(self.position_antenne,self.X_traj,self.Y_traj,self.Z_traj)
            self.thread_gps.trace_trajectoire(self.Latitude,self.Longitude,self.position_antenne)

    def conversion(self,centre,x_tr,y_tr,z_tr):
        print("centre conv",centre)
        print("conversion")
        rayon_terre = 6378137 # rayon moyen de la terre peut etre affiné
        centre = (centre[0]*np.pi/180,centre[1]*np.pi/180)
        x0 = rayon_terre * np.cos(centre[0]) * np.cos(centre[1])
        y0 = rayon_terre * np.cos(centre[0]) * np.sin(centre[1])
        z0 = rayon_terre * np.sin(centre[0])



        X = [x0+X for X in x_tr]
        Y = [y0+Y for Y in y_tr]
        Z = [z0+Z for Z in z_tr]

        Longitude = []
        Latitude = []
        for i in range(len(X)):
            rho =np.sqrt( (X[i]**2)+(Y[i]**2)+(Z[i]**2))
            Longitude_temp = np.arcsin(Z[i]/rho)*180/np.pi
            if Longitude_temp > 90 :
                Longitude_temp = 90 - Longitude_temp
            Longitude.append(Longitude_temp)

            Latitude.append(np.arctan(Y[i]/X[i])*180/np.pi)


        print(Longitude,Latitude)
        return Longitude,Latitude



    def position_antenne_update(self):
        self.thread_centre.update()
        self.position_antenne = self.thread_centre.position_antenne
        #print("position_antenne_update : ", self.position_antenne)


        pass



class thread_position_antenne(QThread):
    """docstring for thread_position_antenne."""

    def __init__(self, fenetre_graph):
        super(thread_position_antenne, self).__init__()
        self.fenetre_graph = fenetre_graph
        self.position_antenne = None

    def run(self):
        pass

    def update(self):
        if self.fenetre_graph.position_antenne is not None :
            self.position_antenne = self.fenetre_graph.position_antenne


class thread_trace_gps(QThread):
    """docstring for thread_trace_gps."""

    def __init__(self, axe,graph):
        super(thread_trace_gps, self).__init__()
        #axe pour tracer la carte
        self.axe = axe
        self.graph = graph
        #
        self.trace = False
        self.i = 0

    def run(self):
        pass

    def gps_carte_fond(self,centre,i):
        self.centre = (centre[0],centre[1])
        if not self.trace:
            #self.centre = (-1.7458099,48.0453455)
            self.marge = 0.003
            self.extent = tilemapbase.Extent.from_lonlat(self.centre[0] - self.marge, self.centre[0] + self.marge,self.centre[1] - self.marge, self.centre[1] + self.marge)
            self.extent = self.extent.to_aspect(1.0)
            self.plotter =  tilemapbase.Plotter(self.extent, tilemapbase.tiles.build_OSM(), width=500, height=500)
            self.trace = True
            self.plotter.plot(self.axe,tilemapbase.tiles.build_OSM())
        #self.plot.show()
            self.graph.draw()
        i += 1
        if i == 500:
            self.trace = False
            i = 0
        return i

    def trace_trajectoire(self,Latitude,Longitude,centre):
        print("trace")
        #self.centre_mean = (np.mean(Longitude),np.mean(Latitude))
        #print(self.centre_mean)
        self.centre = centre
        print("Longitude: ",Longitude)
        print("Lat : ",Latitude)
        self.i = self.gps_carte_fond(centre,self.i)
        if Latitude is not None :
            path = [tilemapbase.project(x,y) for x,y in zip(Longitude,Latitude)]
            x,y = zip(*path)
            #print(x)
            x0,y0 = tilemapbase.project(*self.centre)
            self.axe.plot(x,y,'ro-')
            self.axe.plot(x0,y0,'b>')
            self.axe.axis("off")
            self.graph.draw()
