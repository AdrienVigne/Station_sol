
"""
Acces Sftp pour avoir le moins de modif possible sur la pi



"""
import pysftp



def transfert():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host="192.168.1.45",username = "pi", password = "raspberry",cnopts=cnopts)
    sftp.cwd('/home/pi/Desktop/Drone')
    sftp.put("./trajectoire.csv",'./trajectoire.csv')
    sftp.close()

#transfert()
