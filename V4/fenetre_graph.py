from PySide2.QtWidgets import QMainWindow,QWidget,QPushButton,QVBoxLayout,QApplication,QLabel,QHBoxLayout
from PySide2.QtCore import QThread,QTimer,Qt
from PySide2.QtGui import QPen,QColor
from Client import Client
import pyqtgraph as pg
from donnees import traitement
from time import sleep

recu = None

class Fenetre_graph (QWidget):

    def __init__(self,hote,port,port2):
        super().__init__()


        self.connecte = False
        self.connexion = None
        self.connexion2 = None
        self.hote = hote
        self.port = port
        self.port2 = port2

        self.Liste_shell = []
        self.Matrice = None

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

        self.graphTemp = pg.PlotWidget()
        self.Legend_Temp = self.graphTemp.addLegend()
        self.taille_Temp_x = 100

        self.graphBatt = pg.PlotWidget()
        self.Legend_Batt = self.graphBatt.addLegend()
        self.taille_Batt_x = 100

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


        self.button_sauvegarde = QPushButton("Sauvegarde des données")
        self.button_sauvegarde.clicked.connect(self.sauvergarde)
        self.layout_bouton.addWidget(self.button_sauvegarde)





        self.setLayout(self.layout)

        self.button_connexion.clicked.connect(self.connection)
        self.button_deconnexion.clicked.connect(self.deconnection)



        self.Timer = QTimer()
        self.Timer.timeout.connect(self.text_update)
        #self.Timer.timeout.connect(self.graph_update)
        self.Timer.timeout.connect(self.update)
        self.Timer.timeout.connect(self.text_brute_mise_a_jour)
        self.Timer.setInterval(500)

    def sauvergarde(self):
        self.Donnees.enregistrement()

    def graphAcc_update(self,I,AccX,AccY,AccZ):
        self.graphAcc.clear()

        if (I[-1] > self.taille_Acc_x) :
            self.graphAcc.setXRange(I[-1]-self.taille_Acc_x,I[-1],padding = 0)

        self.graphAcc.plot(I,AccX,pen='r',name="Accelerometre X")
        self.graphAcc.plot(I,AccY,pen='g',name="Accelerometre Y")
        self.graphAcc.plot(I,AccZ,pen='b',name="Accelerometre Z")

    def graphGyro_update(self,I,GyroX,GyroY,GyroZ):
        self.graphGyro.clear()

        if (I[-1] > self.taille_Gyro_x) :
            self.graphGyro.setXRange(I[-1]-self.taille_Gyro_x,I[-1],padding = 0)

        self.graphGyro.plot(I,GyroX,pen='r',name="Gyroscope X")
        self.graphGyro.plot(I,GyroY,pen='g',name="Gyroscope Y")
        self.graphGyro.plot(I,GyroZ,pen='b',name="Gyroscope Z")

    def graphMagneto_update(self,I,MagnetoX,MagnetoY,MagnetoZ):
        self.graphMagneto.clear()

        if (I[-1] > self.taille_Magneto_x) :
            self.graphMagneto.setXRange(I[-1]-self.taille_Magneto_x,I[-1],padding = 0)

        self.graphMagneto.plot(I,MagnetoX,pen='r',name="Magnetometre X")
        self.graphMagneto.plot(I,MagnetoY,pen='g',name="Magnetometre Y")
        self.graphMagneto.plot(I,MagnetoZ,pen='b',name="Magnetometre Z")

    def graphTemp_update(self,I,Temp):
        self.graphTemp.clear()

        if (I[-1] > self.taille_Temp_x) :
            self.graphTemp.setXRange(I[-1]-self.taille_Temp_x,I[-1],padding = 0)

        self.graphTemp.plot(I,Temp,name="Température")

    def graphBatt_update(self,I,Batt):
        self.graphBatt.clear()

        if (I[-1] > self.taille_Batt_x) :
            self.graphBatt.setXRange(I[-1]-self.taille_Batt_x,I[-1],padding = 0)

        self.graphBatt.plot(I,Batt,name="Tension Batterie")


    def graph_update(self):
        #print(recu)
        if recu != 'Attente reception':
            #print("mise a jour ")
            self.Matrice = self.Donnees.matrice(recu)
            self.graphGyro_update(self.Matrice[1:,0],self.Matrice[1:,1],self.Matrice[1:,2],self.Matrice[1:,3])
            self.graphAcc_update(self.Matrice[1:,0],self.Matrice[1:,4],self.Matrice[1:,5],self.Matrice[1:,6])
            self.graphMagneto_update(self.Matrice[1:,0],self.Matrice[1:,7],self.Matrice[1:,8],self.Matrice[1:,9])
            self.graphTemp_update(self.Matrice[1:,0],self.Matrice[1:,-1])
            self.graphBatt_update(self.Matrice[1:,0],self.Matrice[1:,-2])




    def text_update(self):
        recu=self.connexion.reception.decode()

        self.update_graph.recu = recu
        self.update_graph.graph_update()

        self.Text.setText(recu)
        self.Text.setStyleSheet('color : white')


    def text_brute_mise_a_jour(self) :

        recu = str(self.connexion2.reception)
        self.Liste_shell = recu.split('_')
        print(self.Liste_shell)


    def connection(self):
        self.connecte = True
        self.connexion = Client(self.hote,self.port)
        print("connexion")
        self.connexion2 = Client(self.hote,self.port2)
        self.update_graph = graph_thread(self.graphGyro,self.graphAcc,self.graphMagneto,self.graphTemp,self.graphBatt,self.taille_Gyro_x,self.taille_Acc_x,self.taille_Magneto_x,self.taille_Temp_x,self.taille_Batt_x,self.Donnees)
        self.text_thread = Text_MAJ(self.connexion,self.connexion2)

        #print("init du thread")
        self.text_thread.start()
        self.update_graph.start()
        #self.update_graph.start()
        self.Timer.start()
        #print("thread lancé")

    def deconnection(self):
        self.connexion.fin_connexion()
        self.connexion2.fin_connexion()
        self.Timer.stop()

"""
    def update(self):date(self):
        #print("mise a jour")
        #print(self.update_graph.update)
        self.update_graph.update = True
        #print(self.update_graph.update)

"""
class Text_MAJ(QThread):
    def __init__(self,connexion,connexion2):

        super().__init__()

        self.Client = connexion
        self.Client2 = connexion2



    def run(self):
        while 1:

            #print(self.Client)
            recu=self.Client.ecoute()
            recu2=self.Client2.ecoute()

            #print("thread >>"+recu.decode())
            #print("entrée dans le thread")

class graph_thread(QThread):
    recu = None

    def __init__(self,graphGyro,graphAcc,graphMagneto,graphTemp,graphBatt,taille_Gyro_x,taille_Acc_x,taille_Magneto_x,taille_Temp_x,taille_Batt_x,Donnees):
        super().__init__()
        self.graphGyro = graphGyro
        self.graphAcc = graphAcc
        self.graphMagneto = graphMagneto
        self.graphTemp = graphTemp
        self.graphBatt = graphBatt
        self.Donnees  = Donnees
        self.update = False
        self.Matrice = None

        self.taille_Acc_x = taille_Acc_x
        self.taille_Batt_x = taille_Batt_x
        self.taille_Gyro_x = taille_Gyro_x
        self.taille_Temp_x = taille_Temp_x
        self.taille_Magneto_x = taille_Magneto_x



    def run(self):
        """
        while 1 :
            #print(self.update)
            if self.update :
                #print('Mise a jour')
                self.graph_update()
                self.update = False
        """


    def graph_update(self):
        #print("coucou")
        #print(self.recu)
        #self.recu = self.recu.decode()
        if self.recu is not None :
            #print(self.recu)
            #print(self.recu ==  'Attente reception')
            if self.recu != 'Attente reception':
                if type(self.recu) != str:
                    self.recu = self.recu.decode()

                self.Matrice = self.Donnees.matrice(self.recu)
                self.graphGyro_update(self.Matrice[1:,0],self.Matrice[1:,1],self.Matrice[1:,2],self.Matrice[1:,3])
                self.graphAcc_update(self.Matrice[1:,0],self.Matrice[1:,4],self.Matrice[1:,5],self.Matrice[1:,6])
                self.graphMagneto_update(self.Matrice[1:,0],self.Matrice[1:,7],self.Matrice[1:,8],self.Matrice[1:,9])
                self.graphTemp_update(self.Matrice[1:,0],self.Matrice[1:,-1])
                self.graphBatt_update(self.Matrice[1:,0],self.Matrice[1:,-2])

    def graphAcc_update(self,I,AccX,AccY,AccZ):
        self.graphAcc.clear()

        if (I[-1] > self.taille_Acc_x) :
            self.graphAcc.setXRange(I[-1]-self.taille_Acc_x,I[-1],padding = 0)

        self.graphAcc.plot(I,AccX,pen='r',name="Accelerometre X")
        self.graphAcc.plot(I,AccY,pen='g',name="Accelerometre Y")
        self.graphAcc.plot(I,AccZ,pen='b',name="Accelerometre Z")

    def graphGyro_update(self,I,GyroX,GyroY,GyroZ):
        self.graphGyro.clear()

        if (I[-1] > self.taille_Gyro_x) :
            self.graphGyro.setXRange(I[-1]-self.taille_Gyro_x,I[-1],padding = 0)

        self.graphGyro.plot(I,GyroX,pen='r',name="Gyroscope X")
        self.graphGyro.plot(I,GyroY,pen='g',name="Gyroscope Y")
        self.graphGyro.plot(I,GyroZ,pen='b',name="Gyroscope Z")

    def graphMagneto_update(self,I,MagnetoX,MagnetoY,MagnetoZ):
        self.graphMagneto.clear()

        if (I[-1] > self.taille_Magneto_x) :
            self.graphMagneto.setXRange(I[-1]-self.taille_Magneto_x,I[-1],padding = 0)

        self.graphMagneto.plot(I,MagnetoX,pen='r',name="Magnetometre X")
        self.graphMagneto.plot(I,MagnetoY,pen='g',name="Magnetometre Y")
        self.graphMagneto.plot(I,MagnetoZ,pen='b',name="Magnetometre Z")

    def graphTemp_update(self,I,Temp):

        self.graphTemp.clear()

        if (I[-1] > self.taille_Temp_x) :
            self.graphTemp.setXRange(I[-1]-self.taille_Temp_x,I[-1],padding = 0)

        self.graphTemp.plot(I,Temp,name="Température")

    def graphBatt_update(self,I,Batt):
        #print("cc")
        self.graphBatt.clear()

        if (I[-1] > self.taille_Batt_x) :
            self.graphBatt.setXRange(I[-1]-self.taille_Batt_x,I[-1],padding = 0)

        self.graphBatt.plot(I,Batt,name="Tension Batterie")



if __name__ == '__main__':
    app = QApplication([])
    window = Fenetre_graph("192.168.1.6",31000,56880)
    window.show()
    app.exit(app.exec_())
