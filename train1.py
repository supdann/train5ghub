# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 21:10:02 2019
@author: Deepasundar P
"""


import time
import paho.mqtt.client as mqtt



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
client = mqtt.Client("train2")

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
distance_0 = 0

"""Loop"""
while(True):
    while (distance_0>300):


        print(speed)
        """Updating variables"""
        t_end = time.time()
        distance += (speed*(t_end - t_start))/3.6
        t_start = t_end
        
             

        """Publishing variables"""
        client.publish("train/1/leaves", leaves)
        client.publish("train/1/laser", laser)
        client.publish("train//speed", speed)
        client.publish("train/1/distance", distance)
        client.publish("train/1/flag", flag)
        leaves_0 = client.subscribe("train/0/leaves", leaves)
        laser_0 = client.subscribe("train/0/laser", laser)
        speed_0 = client.subscribe("train/0/speed", speed)
        distance_0 = client.subscribe("train/0/distance", distance)
        time.sleep(0.1)
        
        speed = speed_0
        
    distance_0 = client.subscribe("train/0/distance", distance)

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


