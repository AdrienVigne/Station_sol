from PySide2.QtWidgets import QMainWindow,QWidget,QPushButton,QVBoxLayout,QApplication,QLabel,QHBoxLayout,QTextEdit
from PySide2.QtCore import QThread,QTimer,Qt
from PySide2.QtGui import QPen,QColor
from Client import Client



class shell(QWidget):
    """docstring for shell."""

    def __init__(self,fenetre_graph):
        super(shell, self).__init__()

        self.fenetre_graph = fenetre_graph

        p = self.palette()
        self.setAutoFillBackground(True)
        p.setColor(self.backgroundRole(),Qt.black)
        self.setPalette(p)


        #self.connexion2 = Client("192.168.1.70",31000)

        self.text_area = QTextEdit()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_area)
        self.setLayout(self.layout)
        #self.text_area.setAutoFormatting(True)
        self.text_area.setStyleSheet(' background-color : black')
        self.text_area.setTextBackgroundColor(Qt.black)
        self.text_area.setTextColor(Qt.white)
        self.text_area.setReadOnly(True)
        #self.text_area.append("coucou")
        #self.text_area.append("cc")


            #print("init du thread")

        self.affichage_shell = thread_shell(self.text_area,self.fenetre_graph)
        self.affichage_shell.start()
        self.fenetre_graph.Timer.timeout.connect(self.text_update)
        #self.Timer.timeout.connect(self.graph_update)
        #self.Timer.timeout.connect(self.update)
        #self.fenetre_graph.Timer.setInterval(500)
        #self.fenetre_graph.Timer.start()

    def text_update(self):

        self.affichage_shell.text()
        pass






class thread_shell(QThread):
    """docstring for thread_shell."""

    def __init__(self, text,fenetre_graph):
        super(thread_shell, self).__init__()
        self.text_area = text
        self.fenetre_graph = fenetre_graph

    def run(self):
        pass

    def text(self):
        #print("cc")
        L=self.fenetre_graph.Liste_shell

        #print(recu)
        for l in L:
            self.text_area.append(l)








if __name__ == '__main__':
    app = QApplication([])
    window = shell()
    window.show()
    app.exit(app.exec_())
