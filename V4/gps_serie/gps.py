import serial

ser = serial.Serial('/dev/ttyUSB0')

def ConversionDMS2DD(coord,position):
    """ entrée latitude/Longitude,N/S ou E/W"""
    list = coord.split('.')
    deg = float(list[0])//100
    print(deg)
    min = float(list[0])%100
    print(min)
    sec = float(list[1])/100
    print(sec)
    res = float(deg) +float(min)/60 +float(sec)/3600
    if position == "W":
        res = -res
    if position == "S":
        res = -res
    return res




while True :
    msg = ser.readline()
    msg = msg.decode()
    #print(msg)
    L=msg.split(',')
    if L[0]=="$GPGGA":
        ### Conversion degres minutes seconde vers Degres decimaux
        ## formule DEC = DEG+min/60+sec/360
        latitude = ConversionDMS2DD(L[2],L[3])
        print(L[4])
        longitude = ConversionDMS2DD(L[4],L[5])
        print("latitude :",latitude)
        print("Longitude :",longitude)
        print("nombre gps: ",L[7])
