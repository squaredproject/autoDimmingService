#!/usr/bin/env python

from jsonsocket import Client
from datetime import datetime
from time import sleep

host = '127.0.0.1'
port = 5204
dimmingStartHour = 22
dimmingEndHour = 8
dimmedBrightness = 0.25
nonDimmedBrightness = 1

client = Client()
inDimmingMode = False


def setBrightness(newBrightness):
    print "setting Brightness to %s" % newBrightness
    client.connect(host, port)
    client.send(
        {
            "method": "setBrightness",
            "params": {"brightness": newBrightness}
        }
    )
    client.send(
        {
            "method": "loadModel"
        }
    )
    response = client.recv()
    currentBrightness = response['params']['brightness']
    if not(int(currentBrightness * 100) == int(newBrightness * 100)):
        raise Exception("Failed setting brightness, sent %s but got %s" % (currentBrightness, response['brightness']))
    sleep(0.5)
    client.close()


while True:
    t = datetime.now()
    shouldBeInDimmingMode = not (dimmingStartHour > t.hour >= dimmingEndHour)  # assumes the dimming hours span midnight
    if inDimmingMode and not shouldBeInDimmingMode:
        try:
            setBrightness(nonDimmedBrightness)
            inDimmingMode = False
            print "Success"
        except Exception as e:
            print "Error changing brightness"
            print e.message
    if not inDimmingMode and shouldBeInDimmingMode:
        try:
            setBrightness(dimmedBrightness)
            inDimmingMode = True
            print "Success"
        except Exception as e:
            print "Error changing brightness"
            print e.message
    sleep(60)
