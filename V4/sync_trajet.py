from Client import Client

C = Client("192.168.1.45.",31000)

while 1 :
    msg = C.ecoute()
    print(msg.decode())
    if msg == "q":
        C.fin_connexion()
        break
print("fin")
