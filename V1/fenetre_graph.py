from PyQt5.QtWidgets import QMainWindow,QWidget,QPushButton,QVBoxLayout,QApplication,QLabel,QHBoxLayout
from PyQt5.QtCore import QThread,QTimer
from Client import Client
import pyqtgraph as pg
from donnees import traitement

class Fenetre_graph (QWidget):

    def __init__(self,hote,port):
        super().__init__()
        self.connexion = None
        self.hote = hote
        self.port = port
        self.recu = None
        self.Matrice = None

        self.Donnees = traitement()

        self.graphAcc = pg.PlotWidget()
        self.Legend_Acc = self.graphAcc.addLegend()

        self.graphGyro = pg.PlotWidget()
        self.Legend_Gyro = self.graphGyro.addLegend()

        self.graphMagneto = pg.PlotWidget()
        self.Legend_Magneto = self.graphMagneto.addLegend()

        self.graphTemp = pg.PlotWidget()
        self.Legend_Temp = self.graphTemp.addLegend()

        self.graphBatt = pg.PlotWidget()
        self.Legend_Batt = self.graphBatt.addLegend()

        self.layout_centrale_inertielle = QHBoxLayout()
        self.layout_centrale_inertielle.addStretch(1)
        self.layout_centrale_inertielle.addWidget(self.graphAcc)
        self.layout_centrale_inertielle.addWidget(self.graphGyro)
        self.layout_centrale_inertielle.addWidget(self.graphMagneto)

        self.layout_Batt_Temp = QHBoxLayout()

        self.layout_Batt_Temp.addWidget(self.graphTemp)
        self.layout_Batt_Temp.addWidget(self.graphBatt)
        self.layout_Batt_Temp.addStretch(1)


        self.central_widget = QWidget()
        self.button_connexion = QPushButton("Connexion",self.central_widget)
        self.button_deconnexion = QPushButton("Deconnexion",self.central_widget)
        self.Text = QLabel()

        self.layout_bouton = QVBoxLayout()
        self.layout_bouton.addWidget(self.button_connexion)
        self.layout_bouton.addWidget(self.button_deconnexion)
        self.layout_Batt_Temp.addLayout(self.layout_bouton)


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.Text)
        self.layout.addLayout(self.layout_centrale_inertielle)
        self.layout.addLayout(self.layout_Batt_Temp)





        self.setLayout(self.layout)

        self.button_connexion.clicked.connect(self.connection)
        self.button_deconnexion.clicked.connect(self.deconnection)

        self.Timer = QTimer()
        self.Timer.timeout.connect(self.text_update)
        self.Timer.timeout.connect(self.graph_update)
        self.Timer.setInterval(500)


    def graphAcc_update(self,I,AccX,AccY,AccZ):
        self.graphAcc.clear()
        try :
            self.Legend_Acc.scene().removeItem(self.Legend_Acc)
        except:
            print("impossible enleber legend")

        self.Legend_Acc = self.graphAcc.addLegend()
        self.graphAcc.plot(I,AccX,pen='r',name="Accelerometre X")
        self.graphAcc.plot(I,AccY,pen='b',name="Accelerometre Y")
        self.graphAcc.plot(I,AccZ,pen='g',name="Accelerometre Z")

    def graphGyro_update(self,I,GyroX,GyroY,GyroZ):
        self.graphGyro.clear()
        try :
            self.Legend_Gyro.scene().removeItem(self.Legend_Gyro)
        except:
            print("impossible enleber legend")

        self.Legend_Gyro = self.graphGyro.addLegend()
        self.graphGyro.plot(I,GyroX,pen='r',name="Gyroscope X")
        self.graphGyro.plot(I,GyroY,pen='b',name="Gyroscope Y")
        self.graphGyro.plot(I,GyroZ,pen='g',name="Gyroscope Z")

    def graphMagneto_update(self,I,MagnetoX,MagnetoY,MagnetoZ):
        self.graphMagneto.clear()
        try :
            self.Legend_Magneto.scene().removeItem(self.Legend_Magneto)
        except:
            print("impossible enleber legend")

        self.Legend_Magneto = self.graphMagneto.addLegend()
        self.graphMagneto.plot(I,MagnetoX,pen='r',name="Magnetometre X")
        self.graphMagneto.plot(I,MagnetoY,pen='b',name="Magnetometre Y")
        self.graphMagneto.plot(I,MagnetoZ,pen='g',name="Magnetometre Z")

    def graphTemp_update(self,I,Temp):
        self.graphTemp.clear()
        try :
            self.Legend_Temp.scene().removeItem(self.Legend_Temp)
        except:
            print("impossible enleber legend")

        self.Legend_Temp = self.graphTemp.addLegend()
        self.graphTemp.plot(I,Temp,name="Température")

    def graphBatt_update(self,I,Batt):
        self.graphBatt.clear()
        try :
            self.Legend_Batt.scene().removeItem(self.Legend_Batt)
        except:
            print("impossible enleber legend")

        self.Legend_Batt = self.graphBatt.addLegend()
        self.graphBatt.plot(I,Batt,name="Tension Batterie")


    def graph_update(self):
        if self.recu != 'Attente reception':
            self.Matrice = self.Donnees.matrice(self.recu)
            self.graphGyro_update(self.Matrice[1:,0],self.Matrice[1:,1],self.Matrice[1:,2],self.Matrice[1:,3])
            self.graphAcc_update(self.Matrice[1:,0],self.Matrice[1:,4],self.Matrice[1:,5],self.Matrice[1:,6])
            self.graphMagneto_update(self.Matrice[1:,0],self.Matrice[1:,7],self.Matrice[1:,8],self.Matrice[1:,9])
            self.graphTemp_update(self.Matrice[1:,0],self.Matrice[1:,-1])
            self.graphBatt_update(self.Matrice[1:,0],self.Matrice[1:,-2])

        #print("coucou")


    def text_update(self):
        self.recu=self.connexion.reception.decode()

        self.Text.setText(self.recu)

    def connection(self):
        self.connexion = Client(self.hote,self.port)
        print("connexion")

        self.text_thread = Text_MAJ(self.connexion)
        #print("init du thread")
        self.text_thread.start()
        self.Timer.start()
        #print("thread lancé")

    def deconnection(self):
        self.connexion.fin_connexion()

class Text_MAJ(QThread):
    def __init__(self,connexion):

        super().__init__()

        self.Client=connexion


    def run(self):
        while 1:
            #print("coucou")
            #print(self.Client)
            self.recu=self.Client.ecoute()
            #print("thread >>"+self.recu.decode())
            #print("entrée dans le thread")


if __name__ == '__main__':
    app = QApplication([])
    window = Fenetre_graph("192.168.1.70",31000)
    window.show()
    app.exit(app.exec_())
