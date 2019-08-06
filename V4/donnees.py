from numpy import *

class traitement(object):
    """docstring for traitement."""

    def __init__(self):
        super(traitement, self).__init__()
        self.data = []
        self.Matrice = zeros(15)
        self.I = 0

    def matrice(self,recu):
        #print("recu : ",recu)
        self.data = recu[1:len(recu)-3].split(',')

        self.I = self.I+1
        self.data = [self.I]+[float(d) for d in self.data]
        self.data = array(self.data)
        #print(self.Matrice)
        #print("")
        #print(self.data)
        self.Matrice = vstack((self.Matrice,self.data))
        #print("matrice")
        #print(self.Matrice)
        return self.Matrice

    def enregistrement(self):
        savetxt("Donnees.csv",self.Matrice,delimiter = ';' ,header = 'Ordre des données : .... ')
