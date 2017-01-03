#!/usr/bin/env python

import os
import json
import time
import pi_switch
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 17


class OnOff:
    def __init__(self, name, onCode, offCode, rf, iot):
        self.name = name
        self.onCode = onCode
        self.offCode = offCode
        self.rf = rf

        self.shadow = iot.createShadowHandlerWithName(self.name, True)
        self.shadow.shadowRegisterDeltaCallback(self.newShadow)
        self.set(False)

    def set(self, state):
        code = self.onCode if state else self.offCode
        print('Turning %s %s using code %i' % (self.name, 'ON' if state else 'OFF', code))
        self.rf.sendDecimal(code, 24)
        self.shadow.shadowUpdate(json.dumps({
            'state': {
                'reported': {
                    'light': state
                    }
                }
            }
        ), None, 5)

    def newShadow(self, payload, responseStatus, token):
        newState = json.loads(payload)['state']['light']
        self.set(newState)

class Shades:
    def __init__(self, name, upCode, downCode, stopCode, rf, iot):
        self.name = name
        self.upCode = upCode
        self.downCode = downCode
        self.stopCode = stopCode
        self.rf = rf

        self.shadow = iot.createShadowHandlerWithName(self.name, True)
        self.shadow.shadowRegisterDeltaCallback(self.newShadow)
        self.set(upCode)

    def set(self, state):
        code = self.onCode if state else self.offCode
        print('Turning %s %s using code %i' % (self.name, 'ON' if state else 'OFF', code))
        self.rf.sendDecimal(code, 24)
        self.shadow.shadowUpdate(json.dumps({
            'state': {
                'reported': {
                    'light': state
                    }
                }
            }
        ), None, 5)

    def newShadow(self, payload, responseStatus, token):
        newState = json.loads(payload)['state']['light']
        self.set(newState)


def createIoT():
    iot = AWSIoTMQTTShadowClient('AWSHome', useWebsocket=True)
    iot.configureEndpoint('a2uxamo0ohjghy.iot.us-east-1.amazonaws.com', 443)
    iot.configureCredentials(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'root-CA.pem'))
    iot.configureConnectDisconnectTimeout(10)  # 10 sec
    iot.configureMQTTOperationTimeout(5)  # 5 sec
    iot.connect()
    return iot

def createRF():
    rf = pi_switch.RCSwitchSender()
    rf.enableTransmit(0)
    rf.setPulseLength(194)
    return rf

def createGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    return G





if __name__ == "__main__":
    iot = createIoT()
    rf = createRF()

    # Create your switches here, using the format:
    #   OnOff(<THING NAME>, <ON CODE>, <OFF CODE>, rf, iot)
    #
    # Example:
    #   OnOff('floor-lamp', 284099, 284108, rf, iot)
    #
    OnOff('table-lamp', 1398067, 1398076, rf, iot)
    print('Listening...')

    while True:
        time.sleep(0.2)
