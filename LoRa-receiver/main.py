DEBUG=False

from network import LoRa
import socket
import machine
import time
import math
from machine import SD
import os
import pycom
import ubinascii

print('\n(c) Fernando Tejero\n')

# initialise LoRa in LORA mode
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# more params can also be given, like frequency, tx power and spreading factor
sf = 7
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, frequency=868100000, tx_power=3, bandwidth=LoRa.BW_500KHZ, sf=sf, preamble=8, coding_rate=LoRa.CODING_4_5)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Change frequency, spreading factor, coding rate... at any time
lora.frequency(868100000)
lora.sf(7)
lora.coding_rate(LoRa.CODING_4_5)


print('LoRa initialized!')
print('Recibiendo numero de paquetes:')
#s.setblocking(True)
#iteraciones = s.recv(256)
#print('...')
#print('Numero de iteraciones: '+ str(iteraciones))
#s.setblocking(False)

s.setblocking(True)
tamano = s.recv(256)
print("tamano: " + str(tamano))
#iteraciones = s.recv(256)
#print("iteraciones: " + str(iteraciones))
#s.setblocking(False)

def string_to_int(s):
    try:
        temp = int(eval(str(s)))
        if type(temp) == int:
            return temp
    except:
        return

#iteraciones = string_to_int(iteraciones)
tamano = string_to_int(tamano)
print('Tamano: ' + str(tamano))

imagen = bytearray()
datos = 0
i=0
inicio = 0
#final = inicio+contador-1
contador_nuevo = 0
contador_viejo = 0
#iteraciones = 100
tamano_total = 0
contador_forz = 0

while tamano_total<tamano:
    i = i+1
    s.setblocking(True)
    #if i%10==0:
        #print('Paquete numero '+ str(i))
    datos = s.recv(150)
    s.setblocking(False)
    #print('Paquete ' + str(i) + ': ' + ubinascii.hexlify(datos).decode('utf-. 8'))
    contador_nuevo = contador_nuevo+len(datos)
    tamano_total = tamano_total+len(datos)
    print('Tamano paquete recibido: ' + str(len(datos)))
    #print('Tamano total: ' + str(tamano_total))
    #print('Tamano paquete: ' + str(len(datos)))
    #imagen = imagen+datos #linea inutil
    imagen[contador_viejo:(contador_nuevo-1)] = datos
    contador_viejo = contador_nuevo
    #if contador_nuevo!=len(datos)

    #if i%10==0:
    #    print('Iteracion numero: ' +str(i))
    #print('Bytes:' + str(len(datos)))
    #if i==iteraciones:
    #    final = tamano
    #    print('Tamaño ultimo paquete: ' + str((iteraciones*contador)-tamano))
    #print('Tamaño imagen actual: ' + str(len(imagen)))
    #if i==iteraciones:
    #    print('Imagen enviada con exito.')
    #s.setblocking(False)

#Guardar la imagen en la tarjeta SD
sd = SD()
os.mount(sd,'/sd')
os.listdir('/sd')

pycom.heartbeat(False)
f = open('/sd/test.recibida.jpg','w')
print('Guardando imagen... ')
f.write(imagen)
print('Imagen guardada.')
f.close()
#while True:
#    data=s.recv(64)
    #data_2=data.decode("utf-8")
#    if data != b'':
        #print(data_2);
#        f.write(imagen)
#        print('Imagen guardada.')
#        f.close()
        #f.flush()
