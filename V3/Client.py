import socket,sys

class Client(object):
    """docstring for Client."""

    def __init__(self,host , port):
        super(Client, self).__init__()
        self.port = port
        self.host = host
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.reception = b'Attente reception'
        try :
            self.sock.connect((host,port))
        except socket.error:
            print("La connexion est impossible")
            sys.exit()
        print("Connexion établie  avec le serveur ")

    def ecoute(self):
        #print("coucou reception msg")
        self.reception = self.sock.recv(1024)
        #print("Client : ",self.reception)
        #print(self.reception)
        #print("fin reception")
        return self.reception

    def envoie(self,msg):
        print("msg a envoyer",msg)
        MSG = msg.encode()
        self.sock.send(MSG)

    def fin_connexion(self):
        self.sock.close()


if __name__=='__main__':
    C=Client("192.168.1.70",31000)
    while 1:
        print(C.ecoute())
        print("")
