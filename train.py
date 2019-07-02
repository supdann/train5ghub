# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 21:10:02 2019
@author: Deepasundar P
"""

import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt



"""RPi setup"""
GPIO.setmode(GPIO.BCM)


#GPIO.setup(ECHO,GPIO.IN)

ECHO = 23

def control(speed):
    return speed-1
"""MQTT FUNCTIONS"""
def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_connect(client, userdata, flags, rc):
    if (rc==0):
        print("Connected OK")
    else:
        print("Bad connection returned code=", rc)

def on_disconnect(client, userdata, flags, rc = 0):
    print("Disconnected result code "+str(rc))

"""MQTT setup"""
broker = "10.1.1.222"
client = mqtt.Client("train1")

client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_log=on_log

print("Connecting to broker ", broker)

client.connect(broker)
client.loop_start()

"""Initiation of variables"""
proximity =  20
distance = 0
speed = 150 #Km/Hr
leaves = False
laser = False
t_start = time.time()
flag = 1

"""Loop"""
while (True):

    GPIO.setup(ECHO,GPIO.OUT)

    """Calculating distance"""
    GPIO.output(ECHO, True)
    time.sleep(0.00001)
    GPIO.output(ECHO, False)

    GPIO.setup(ECHO,GPIO.IN)
    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    sig_time = end - start

    proximity = sig_time / 0.000058
    print(speed)
    """Updating variables"""
    t_end = time.time()
    distance += (speed*(t_end - t_start))/3.6
    t_start = t_end
    
    if proximity <= 10:
         leaves = True
         while(speed!=100):
             speed = speed-0.5
             flag = 0
             client.publish("train/0/speed", speed)
             client.publish("train/0/flag", flag)
             print('Speed down:', speed)
             time.sleep(0.01)
         laser = True

    else:
         leaves = False
         
         while(speed!=150):
             speed = speed+0.5
             flag = 1
             client.publish("train/0/speed", speed)
             print('Speed up:', speed)
             client.publish("train/0/flag", flag)
             time.sleep(0.01)
         laser = False
     

    """Publishing variables"""
    client.publish("train/0/leaves", leaves)
    client.publish("train/0/laser", laser)
    client.publish("train/0/speed", speed)
    client.publish("train/0/distance", distance)
    client.publish("train/0/flag", flag)
    #leaves_1 = client.subscribe("train/1/leaves", leaves)
    #laser_1 = client.subscribe("train/1/laser", laser)
    #speed_1 = client.subs("train/1/speed", speed)
    #distance_1 = client.publish("train/1/distance", distance)
    time.sleep(0.1)
    
    #speed = speed_1

client.loop_stop()
client.disconnect()


# =============================================================================
#     if distance <= 10:
#         sensor_temp = True
#         speed_temp = 100
#         brush_temp = True
#
#     else:
#         sensor_temp = False
#         speed_temp = 150
#         brush_temp = False
#
#     if sensor_temp != sensor:
#         client.publish("Hub/train1/sensor", sensor_temp)
#         client.publish("Hub/train1/sensor", brush_temp)
#         client.publish("Hub/train1/sensor", speed_temp)
#
#     sensor = sensor_temp
#     brush = brush_temp
#     speed = speed_temp
# =============================================================================

