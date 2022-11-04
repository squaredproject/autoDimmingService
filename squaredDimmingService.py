#!/usr/bin/env python

from jsonsocket import Client
from datetime import datetime
from time import sleep

host = '127.0.0.1'
port = 5204
dimmingStartHour =  7
dimmingEndHour = 8
dimmedBrightness = 1
nonDimmedBrightness = 1

client = Client()
inDimmingMode = False


def setBrightness(newBrightness):
    print("setting Brightness to %s" % newBrightness)
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
    print(f'inDimmingMode {inDimmingMode} shouldBeInDimmingMode {shouldBeInDimmingMode}')
    if inDimmingMode and not shouldBeInDimmingMode: 
        try:
            setBrightness(nonDimmedBrightness)
            inDimmingMode = False
            print("Success")
        except Exception as e:
            print("Error changing brightness")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
    if not inDimmingMode and shouldBeInDimmingMode:
        try:
            setBrightness(dimmedBrightness)
            inDimmingMode = True
            print("Success")
        except Exception as e:
            print("Error changing brightness")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
    sleep(60)
