import os
from PySide2.QtWidgets import QLabel, QVBoxLayout, QApplication, QWidget,QHBoxLayout

from PySide2.QtCore import QThread
from pyqtgraph.widgets import MatplotlibWidget as mw
import tilemapbase
import numpy as np

import pyqtgraph as pg

class Affichage_GPS(QWidget):
    """docstring for Affichage_GPS."""

    def __init__(self, fen1,Timer):
        super(Affichage_GPS, self).__init__()
        self.fenetre_graph = fen1

        tilemapbase.init(create=True)
        #self.affichage_carte = False
        self.Latitude = []
        self.Longitude = []
        self.Altitude = []
        self.Position = []

        self.graph = mw.MatplotlibWidget(size=(2,2),dpi=300)
        self.plot = self.graph.getFigure()
        #self.plot2 = self.plot.subplots(figsize=(8, 8), dpi=300)
        self.graph.resize(800,800)

        self.axe = self.plot.add_subplot(111)
        self.axe.axis("off")
        #self.axe.resize(800,800)
        #self.graph.set

        self.position_antenne = None

        """
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.graph)
        self.setLayout(self.layout)
        """

        self.thread_gps = gps_thread(self.Latitude,self.Longitude,self.Altitude,self.Position,self.axe,self.fenetre_graph,self.graph)
        self.thread_gps.setTerminationEnabled(True)
        self.thread_gps.start()


        #self.Timer.timeout.connect(self.gps_update)
        #self.Timer.timeout.connect(self.thread_gps.variable_update())
        #self.Timer.timeout.connect(self.gps_carte_fond)
        self.fenetre_graph.Timer.timeout.connect(self.gps_update)

        self.graph_altitude = pg.PlotWidget()
        self.Legend_Altitude =self.graph_altitude.addLegend()
        self.taille_altitude = 100


        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.graph)
        self.hbox.addWidget(self.graph_altitude)
        self.hbox.addStretch(1)
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

        self.update_altitude = thread_altitude(self.graph_altitude,self.taille_altitude,self.thread_gps)
        self.update_altitude.start()







    def gps_update(self):
        #print("entre fct")
        self.thread_gps.gps_waypoints()
        self.update_altitude.graph_update()
        pass


class thread_altitude(QThread):
    """docstring for graph_altitude."""

    def __init__(self, graph_altitude,taille_altitude,gps_thread):
        super(thread_altitude, self).__init__()
        self.graph_altitude = graph_altitude
        self.taille_altitude = taille_altitude
        self.gps_thread = gps_thread
        self.X = [0]



    def run(self):
        pass

    def graph_update(self):

        #print(self.gps_thread.Altitude)
        #print(self.X)
        if self.gps_thread.Altitude is not [] :

            #print(self.recu)
            #print(self.recu ==  'Attente reception')
            self.graphAlti_update(self.gps_thread.Altitude)
            self.X.append(self.X[-1]+1)
            #print("X;",self.X)

    def graphAlti_update(self,Alti):
        self.graph_altitude.clear()

        if (self.X[-1] > self.taille_altitude) :
            self.graph_altitude.setXRange(self.X[-1]-self.taille_altitude,self.X[-1],padding = 0)

        self.graph_altitude.plot(self.X,Alti,pen='r',name="Altitude (m)")
        #print("coucou")






class gps_thread(QThread):
    """docstring for gps_thread."""

    def __init__(self, Latitude,Longitude,Altitude,Position,axe,fen1,graph):
        super(gps_thread, self).__init__()
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Altitude = Altitude
        self.Position = Position
        self.axe = axe
        self.fenetre_graph = fen1
        self.matrice = None
        self.graph = graph
        self.trace = False
        self.position_antenne = None
        self.i = 0

    def run(self):
        pass

    def variable_update(self):

        if self.fenetre_graph.update_graph is not None :
            if self.fenetre_graph.update_graph.Matrice is not None :
                #print(self.fenetre_graph.update_graph.Matrice)
                self.matrice = self.fenetre_graph.update_graph.Matrice
        #print('coucou')
        #print(self.fenetre_graph.update_graph.Matrice is None)
        #print(self.matrice is not None)
        if self.matrice is not None :
            self.Latitude = self.matrice[1:,10]
            self.Longitude = self.matrice[1:,11]
            self.Altitude = self.matrice[1:,12]
            self.position_antenne = self.fenetre_graph.position_antenne
            #print("coucou")
            #print(type(self.Latitude))
            #print(self.Latitude.shape)

    def gps_carte_fond(self,i):
        #print(self.fenetre_graph.Matrice)

        #print(self.Longitude,self.Latitude)
        #rint(self.matrice is not None)
        if not self.trace:
            if self.matrice is not None :
            #print('tracé')

                if None is not None :
                    self.centre = (self.position_antenne[1],self.position_antenne[0])

                else :
                    self.centre = (np.mean(self.Longitude[0]),np.mean(self.Latitude[0]))
                    print("centre : ",self.centre)
                print("self.position_antenne :",self.position_antenne)
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
        #self.affichage_carte = True
        #self.fig ,self.ax =







    def gps_waypoints(self):
        self.variable_update()
        #print("cc")
        if self.matrice is not None :
            #self.axe.clear()
        #self.affichage_carte = False

            self.i=self.gps_carte_fond(self.i)
        #print("nouveau point")
            path = [tilemapbase.project(x,y) for x,y in zip(self.Longitude,self.Latitude)]
            x, y = zip(*path)
            self.axe.plot(x,y,'ro-')
            self.axe.axis("off")
            self.graph.draw()







if __name__ == '__main__':
    app = QApplication([])

    window = Affichage_GPS()
    window.show()
    app.exit(app.exec_())
