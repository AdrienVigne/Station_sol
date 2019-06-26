import os
from PySide2.QtWidgets import QLabel, QVBoxLayout, QApplication, QWidget
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import QUrl
from pyqtgraph.widgets import MatplotlibWidget as mw
import tilemapbase

class Affichage_GPS(QWidget):
    """docstring for Affichage_GPS."""

    def __init__(self, fen1,Timer):
        super(Affichage_GPS, self).__init__()
        self.fenetre_graph = fen1
        self.Timer = Timer
        tilemapbase.init(create=True)
        self.affichage_carte = False
        self.Latitude = []
        self.Longitude = []
        self.Altitude = []
        self.Position = []

        self.graph = mw.MatplotlibWidget()
        self.plot = self.graph.getFigure()
        #self.plot2 = self.plot.subplots(figsize=(8, 8), dpi=100)
        self.graph.resize(400,400)

        self.axe = self.plot.add_subplot(111)
        self.axe.axis("off")
        #self.axe.resize(800,800)
        #self.graph.set




        self.layout = QVBoxLayout()
        self.layout.addWidget(self.graph)
        self.setLayout(self.layout)


        #self.Timer.timeout.connect(self.gps_update)
        self.Timer.timeout.connect(self.variable_update)
        #self.Timer.timeout.connect(self.gps_carte_fond)
        self.Timer.timeout.connect(self.gps_waypoints)

    def variable_update(self):
        if self.fenetre_graph.Matrice is not None :
            self.Latitude = self.fenetre_graph.Matrice[1:,10]
            self.Longitude = self.fenetre_graph.Matrice[1:,11]
            self.Altitude = self.fenetre_graph.Matrice[1:,12]

            #print(type(self.Latitude))
            #print(self.Latitude.shape)

    def gps_carte_fond(self):
        #print(self.fenetre_graph.Matrice)

        if self.fenetre_graph.Matrice is not None :
            #print(self.Longitude,self.Latitude)
            self.centre = (self.Longitude[0],self.Latitude[0])
            #self.centre = (-1.7458099,48.0453455)
            self.marge = 0.002
            self.extent = tilemapbase.Extent.from_lonlat(self.centre[0] - self.marge, self.centre[0] + self.marge,self.centre[1] - self.marge, self.centre[1] + self.marge)
            self.extent = self.extent.to_aspect(1.0)
            self.plotter =  tilemapbase.Plotter(self.extent, tilemapbase.tiles.build_OSM(), width=400)
            self.plotter.plot(self.axe,tilemapbase.tiles.build_OSM())
            #self.plot.show()
            self.graph.draw()
            self.affichage_carte = True
            #self.fig ,self.ax =







    def gps_waypoints(self):
        if self.fenetre_graph.Matrice is not None :
            self.axe.clear()
        #self.affichage_carte = False
            self.gps_carte_fond()
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
