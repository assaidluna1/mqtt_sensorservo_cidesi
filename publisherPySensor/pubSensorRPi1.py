#******************************************************************************#
# Publisher Sensor a Broker MQTT v1.0                                          #
# Elaborado por: Assaid Luna, para I+D MC Microcomputación                     #
# Publiser a Broker MQTT de Datos de sensor adquiridos vía comunicación serial #
# Ejecutable en plataformas Python V3.X+                                       #
# Taller IoT para CIDESI, septiembre 1 de 2023                                 #
#******************************************************************************#

#******************************************************************************#
# Importamos librerías, se requiere instalación previa de Paho MQTT y PySerial
import random
import time
from paho.mqtt import client as mqtt_client
import sys, time, signal
import serial

#******************************************************************************#
# Asigna nombre de puerto físico USB a variable. 
# Verificar puerto USB en sistemas Linux, Mac o MS-Windows
serial_portname = '/dev/ttyUSB0'

#******************************************************************************#
# Se definen las variables de ambiente Broker MQTT, 
# para el taller no es necesario definir usuario y contraseña
broker = '8.210.144.18'
port = 1883
topic = "cidesi/laboratorio/robotica/"
client_id = 'publisher-001'
# usuario = 'emqx'
# password = 'public'

#******************************************************************************#
# Conexión serial y asignación a variable
serial_port = serial.Serial(serial_portname, baudrate=9600, timeout=2.0)
time.sleep(0.2)

#******************************************************************************#
# Función de comunicación con Broker MQTT, 
# no se necesitan banderas para el taller
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conexión establecida con el Broker")
        else:
            print("Fallo, no se ha logrado la comunicación con código: %d\n", rc)
    # Asignación de datos de cliente .
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(usuario, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#******************************************************************************#
# Función para envío de mensaje a Broker MQTT, se lee el dato serial, 
# se asigna a variable input y se envía como mensaje al topic asignado
def publish(client):
    #Inicia en 10, son los grados con los que se inicia el mov de servomotor
    input_message = 10
    while True:
        input_message = serial_port.readline().decode(encoding='ascii',errors='ignore').rstrip()
        msg = f"{input_message}"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Se ha enviado el mensaje `{msg}` al topic `{topic}`")
        else:
            print(f"Ha fallado el envío de mensaje al topic: {topic}")

#******************************************************************************#
# Función de ejecución de funciones y loop, se llama secuencialmente y se 
# ejecutan en orden, con un loop que permite la constante ejecución con una 
# espera de 2 segundos entre envío de mensajes
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()
    time.sleep(2000)

#******************************************************************************#
# Función principal, llama a función de ejecución run
if __name__ == '__main__':
    run()

#******************************************************************************#
# Se limpia y libera el puerto
serial_port.close()