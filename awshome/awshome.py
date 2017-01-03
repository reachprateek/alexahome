#!/usr/bin/env python

import os
import json
import time
import pi_switch
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 17

#family room shades
fr_ch0_open = '0100100000110001111100110101000000011110'
fr_ch0_close = '0100100000110001111100110101000000111100'
fr_ch0_stop = '0100100000110001111100110101000001010101'


fr_ch1_open = '0100100000110001111100110101000100011110'
fr_ch1_close = '0100100000110001111100110101000100111100'
fr_ch1_stop = '0100100000110001111100110101000101010101'


fr_ch2_open = '0100100000110001111100110101001000011110'
fr_ch2_close = '0100100000110001111100110101001000111100'
fr_ch2_stop = '0100100000110001111100110101001001010101'


fr_ch3_open = '0100100000110001111100110101001100011110'
fr_ch3_close = '0100100000110001111100110101001100111100'
fr_ch3_stop = '0100100000110001111100110101001101010101'


fr_ch4_open = '0100100000110001111100110101010000011110'
fr_ch4_close = '0100100000110001111100110101010000110011'
fr_ch4_stop = '0100100000110001111100110101010001010101'

#bedrooms
br_ch0_open = '1101000000110001001101110010000000010001'
br_ch0_close = '1101000000110001001101110010000000110011'
br_ch0_stop = '1101000000110001001101110010000001010101'

#study room shade
sr_ch1_open = '1101000000110001001101110010000100010001'
sr_ch1_close = '1101000000110001001101110010000100110011'
sr_ch1_stop = '1101000000110001001101110010000101010101'

#aarav room shade
ar_ch2_open = '1101000000110001001101110010001000010001'
ar_ch2_close = '1101000000110001001101110010001000110011'
ar_ch2_stop = '1101000000110001001101110010001001010101'


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

    starter = 0.0047
    time_to_first_bit_delay = 0.0015
    zero = 0.00028
    one = 0.00062
    after_zero_delay = 0.0008
    after_one_delay = 0.00045
    extended_delay = 0.01

    def __init__(self, name, openCode, closeCode, stopCode, gpio, iot):
        self.name = name
        self.openCode = openCode
        self.closeCode = closeCode
        self.stopCode = stopCode
        self.gpio = gpio

        self.shadow = iot.createShadowHandlerWithName(self.name, True)
        self.shadow.shadowRegisterDeltaCallback(self.newShadow)
        self.set('OPEN')

    def set(self, state):
        choices = {'OPEN': self.openCode, 'CLOSE': self.closeCode, 'STOP': self.stopCode}
        code = choices.get(state, self.stopCode)
        print('Turning %s %s using code %s' % (self.name, state, code))
        self.transmit_code(code)
        self.shadow.shadowUpdate(json.dumps({
            'state': {
                'reported': {
                    'shade': state
                    }
                }
            }
        ), None, 5)

    def transmit_code(self, code):
        for t in range(NUM_ATTEMPTS):
            self.sendSignal(self.starter)
            time.sleep(self.time_to_first_bit_delay)
            for i in code:
                if i == '0':
                    self.sendSignal( self.zero)
                    time.sleep(self.after_zero_delay)
                elif i == '1':
                    self.sendSignal(self.one)
                    time.sleep(self.after_one_delay)
                else:
                    continue
        self.gpio.cleanup()

    def sendSignal(self, length):
        self.gpio.output(TRANSMIT_PIN, 1)
        time.sleep(length)
        self.gpio.output(TRANSMIT_PIN, 0)        

    def newShadow(self, payload, responseStatus, token):
        newState = json.loads(payload)['state']['shade']
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
    return GPIO    

if __name__ == "__main__":
    iot = createIoT()
    rf = createRF()
    gpio = createGPIO()


    # Create your switches here, using the format:
    #   OnOff(<THING NAME>, <ON CODE>, <OFF CODE>, rf, iot)
    #
    # Example:
    #   OnOff('floor-lamp', 284099, 284108, rf, iot)
    #
    #lamps
    #OnOff('table-lamp', 1398067, 1398076, rf, iot)

    #shades family-room
    #Shades('family-room-shades', fr_ch0_open, fr_ch0_close, fr_ch0_stop, gpio, iot)
    #Shades('family-room-shade1', fr_ch1_open, fr_ch1_close, fr_ch1_stop, gpio, iot)
    #Shades('family-room-shade2', fr_ch2_open, fr_ch2_close, fr_ch2_stop, gpio, iot)    
    #Shades('family-room-shade3', fr_ch3_open, fr_ch3_close, fr_ch3_stop, gpio, iot)        
    #Shades('family-room-shade4', fr_ch4_open, fr_ch4_close, fr_ch4_stop, gpio, iot)

    #shades bedrooms
    #Shades('bedroom-shades', br_ch0_open, br_ch0_close, br_ch0_stop, gpio, iot)
    Shades('study-room-shade', sr_ch1_open, sr_ch1_close, sr_ch1_stop, gpio, iot)
    #Shades('aarav-room-shade', ar_ch2_open, ar_ch2_close, ar_ch2_stop, gpio, iot)

    print('Listening...')

    while True:
        time.sleep(0.2)
