import socket
import datetime
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

def get_BLT_MAC(device_array, device_name):
    print(":: GET MAC ::")
    for  addr, name in device_array:
        if device_name == name: 
            print (" Device Trouve ! [%s : %s]" %(name,addr))
            return addr

def getBltFrame ():
    print(" R : ")

class measure_data:
    def __init__(self, date, accel, gyro, temp):
        self.date = date
        self.accel = accel
        self.gyro = gyro
        self.temp = temp
    def print_data(self):
        print("["+self.date.strftime('%d/%m/%y %I:%M %S %p')+"] accel("+self.accel[0]+";"+self.accel[1]+";"+self.accel[2]+")"+"  gyro("+self.gyro[0]+";"+self.gyro[1]+";"+self.gyro[2]+")"+"  temp :"+self.temp+"c")



# On scan les device a la recherche du M5Stick: ESP32test
#arrayDeviceBLT=scan_BLT()

m5_name="ESP32test"
#m5_mac=get_BLT_MAC(arrayDeviceBLT,m5_name)
m5_mac="50:02:91:8D:D7:72"



client_socket=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

client_socket.connect((m5_mac,1))

size = 1024 
rcv=10
datas=[rcv]
while rcv>0:
    data = client_socket.recv(size).decode('UTF-8')
    if len(data) <5:
        print(" false ")
        continue
    array_data=data.split(',')
    measure_data(datetime.datetime.now(),array_data[0:3],array_data[3:6],array_data[6]).print_data()
    rcv-=1  
    #print(array_data)

client_socket.close()

