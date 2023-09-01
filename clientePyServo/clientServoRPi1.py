#******************************************************************************#
# Cliente de Broker MQTT a ejecución en servo v1.0                             #
# Elaborado por: Assaid Luna, para I+D MC Microcomputación                     #
# Cliente que adquiere data de Broker MQTT y gira eje de servo motor           #
# Ejecutable en plataformas Python V3.X+                                       #
# Taller IoT para CIDESI, septiembre 1 de 2023                                 #
#******************************************************************************#

#******************************************************************************#
# Importamos librerías, se requiere instalación previa de GPIO, ejecutable en 
# plataformas Raspberry Pi y otras SBC compatibles con libreria y GPIO
import ssl
import sys
import RPi.GPIO as GPIO
import time
import paho.mqtt.client

#******************************************************************************#
# Inicialización de servo, para evitar vibración
# Servo conectado a pin 17 de GPIO
SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
ServoPin = 17
#Definimos el ángulo máximo y mínimo del servo
def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servoPIN, GPIO.OUT)
#p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
#p.start(2.5) # Initialization


#******************************************************************************#
# Función de configuración de Servo en pin 17
def setup():
    global p
    GPIO.setmode(GPIO.BCM)       
    GPIO.setup(ServoPin, GPIO.OUT)   # pin como salida
    GPIO.output(ServoPin, GPIO.LOW)  # Se define pin como bajo o LOW
    p = GPIO.PWM(ServoPin, 50)     # Frecuencia Servo 50Hz
    p.start(0)                     # Ciclo = 0

#******************************************************************************#
# Función de configuración de movimiento de Servo, de 0 a 180 grados por PWM
def setAngle(angle): 
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)#map the angle to duty cycle and output it

#******************************************************************************#
# Función de comunicación con Broker MQTT, se suscribe al topic definido
def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='cidesi/laboratorio/robotica/', qos=2)

#******************************************************************************#
# Función de recepción de data, asignación a variables y normalización del 
# dato para que no supere el movimiento de 0 a 180 grados
def on_message(client, userdata, message):
	angulo = int(int(message.payload)*(179/1023))
	print('------------------------------')
	print('topic: %s' % message.topic)
	print('payload: %s' % message.payload)
	print('qos: %d' % message.qos)
	print(angulo)
	setAngle(angulo)

#******************************************************************************#
# Función de limpieza y liberación de pin (evitamos que el servo se desgaste)
def destroy():
    p.stop()
    GPIO.cleanup()

#******************************************************************************#
# Función "principal" de ejecución, llama de manera ordenada a las demás 
# funciones y mantiene un ciclo hasta que se corte el proceso con Control + C
def main():
	client = paho.mqtt.client.Client(client_id='CIDESI_mqtt_lab1', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='8.210.144.18', port=1883)
	client.loop_forever()
        
#******************************************************************************#
# Se ejecuta la función principal hasta que se corte el proceso
if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the program destroy() will be executed.
        destroy()

sys.exit(0)