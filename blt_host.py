import socket
import datetime
import mariadb 
import sys
from bluetooth import *


#@brief : Scan for available blt  devices
#@return : Array of available devices 
def scan_BLT():
    count=0
    print(": SCAN BLT DEVICES ::")
    nearby_devices = discover_devices(lookup_names = True)
    for name, addr in nearby_devices:
        count+=1
        print ("(%d) -  %s - %s" % (count, addr, name))
#        print([_ for _ in find_service(address=name) if 'RFCOMM' in _['protocol']]) 
    return nearby_devices


# Get Mac adress of a named device
def get_BLT_MAC(device_array, device_name):
    print(":: GET MAC ::")
    for  addr, name in device_array:
        if device_name == name: 
            print (" Device Trouve ! [%s : %s]" %(name,addr))
            return addr


# Repreasentation of data 
class measure_data:
    date=0
    accel=0
    gyro=0
    temp=0
    def __init__(self, date, gyro, accel,  temp):
        self.date = date
        self.accel = accel
        self.gyro = gyro
        self.temp = temp
    def print_data(self):
        print("["+self.date.strftime('%d/%m/%y %I:%M %S %p')+"] accel("+self.accel[0]+";"+self.accel[1]+";"+self.accel[2]+")"+"  gyro("+self.gyro[0]+";"+self.gyro[1]+";"+self.gyro[2]+")"+"  temp :"+self.temp+"c")


# :::::::::::::::::::::::::::::: MAIN ::::::::::::::::::::::


# COnection a mariadb 
try:
    conn = mariadb.connect(
        user="rasp",
        password="raspmdp",
        host="localhost",
        port=3306,
        database="m5data")
    conn.autocommit= True
except mariadb.Error as e:
    print(f"Error Conecting to MariaDB PLATEFORM: {e}")
    sys.exit(1)
cur = conn.cursor()
# On scan les device a la recherche du M5Stick: ESP32test

m5_name="ESP32test"
#m5_mac = get_BLT_MAC(arrayDeviceBLT=scan_BLT(),m5_name)
m5_mac="50:02:91:8D:D7:72"


client_socket=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

client_socket.connect((m5_mac,1))

size = 1024
rcv=10
datas=[rcv]
while rcv>0:
    data = client_socket.recv(size).decode('UTF-8')
    if len(data) <5:
        continue
    array_data=data.split(',')
    data_obj=measure_data(datetime.datetime.now(),array_data[0:3],array_data[3:6],array_data[6])
    data_obj.print_data()
    try:
        cur.execute(
            "INSERT INTO data (date,accelX,accelY,accelZ,gyromX,gyromY,gyromZ,temp) VALUES (?,?,?,?,?,?,?,?)",
            (getattr(data_obj,'date'),
             float(getattr(data_obj,'accel')[0]),
             float(getattr(data_obj,'accel')[1]),
             float(getattr(data_obj,'accel')[2]),
             float(getattr(data_obj,'gyro')[0]),
             float(getattr(data_obj,'gyro')[1]),
             float(getattr(data_obj,'gyro')[2]),
             float(getattr(data_obj,'temp'))))
    except mariadb.Error as e:
        print("Error : {e}")
    print(f"Data num {cur.lastrowid}")
    rcv-=1
conn.close()
client_socket.close()

