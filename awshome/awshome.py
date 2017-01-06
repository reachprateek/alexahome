#!/usr/bin/env python

import os
import json
import time
import pi_switch
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

NUM_ATTEMPTS = 9
TRANSMIT_PIN = 17

#family room shades
fr_ch0_off = '0100100000110001111100110101000000011110'
fr_ch0_on = '0100100000110001111100110101000000111100'
fr_ch0_stop = '0100100000110001111100110101000001010101'


fr_ch1_off = '0100100000110001111100110101000100011110'
fr_ch1_on = '0100100000110001111100110101000100111100'
fr_ch1_stop = '0100100000110001111100110101000101010101'


fr_ch2_off = '0100100000110001111100110101001000011110'
fr_ch2_on = '0100100000110001111100110101001000111100'
fr_ch2_stop = '0100100000110001111100110101001001010101'


fr_ch3_off = '0100100000110001111100110101001100011110'
fr_ch3_on = '0100100000110001111100110101001100111100'
fr_ch3_stop = '0100100000110001111100110101001101010101'


fr_ch4_off = '0100100000110001111100110101010000011110'
fr_ch4_on = '0100100000110001111100110101010000110011'
fr_ch4_stop = '0100100000110001111100110101010001010101'

#bedrooms
br_ch0_off = '1101000000110001001101110010000000010001'
br_ch0_on = '1101000000110001001101110010000000110011'
br_ch0_stop = '1101000000110001001101110010000001010101'

#study room shade
sr_ch1_off = '1101000000110001001101110010000100010001'
sr_ch1_on = '1101000000110001001101110010000100110011'
sr_ch1_stop = '1101000000110001001101110010000101010101'

#aarav room shade
ar_ch2_off = '1101000000110001001101110010001000010001'
ar_ch2_on = '1101000000110001001101110010001000110011'
ar_ch2_stop = '1101000000110001001101110010001001010101'

'''
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
'''
class Shades:

    starter = 0.0047
    time_to_first_bit_delay = 0.0015
    zero = 0.00028
    one = 0.00062
    after_zero_delay = 0.0008
    after_one_delay = 0.00045
    extended_delay = 0.015

    def __init__(self, name, offCode, onCode, stopCode, iot):
        self.name = name
        self.offCode = offCode
        self.onCode = onCode
        self.stopCode = stopCode

        self.shadow = iot.createShadowHandlerWithName(self.name, True)
        self.shadow.shadowRegisterDeltaCallback(self.newShadow)
        #self.set('OFF')

    def set(self, state):
        choices = {'OFF': self.offCode, 'ON': self.onCode, 'STOP': self.stopCode}
        code = choices.get(state, self.stopCode)
        print('Turning %s %s using code %s' % (self.name, state, code))
        transmit_code(self, code)
        self.shadow.shadowUpdate(json.dumps({
            'state': {
                'reported': {
                    'shade': state
                    }
                }
            }
        ), None, 5)

    def newShadow(self, payload, responseStatus, token):
        newState = json.loads(payload)['state']['shade']
        self.set(newState)

def transmit_code(shade, code):
    for t in range(NUM_ATTEMPTS):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
        sendSignal(shade.starter)
        time.sleep(shade.time_to_first_bit_delay)
        for i in code:
            if i == '0':
                sendSignal(shade.zero)
                time.sleep(shade.after_zero_delay)
            elif i == '1':
                sendSignal(shade.one)
                time.sleep(shade.after_one_delay)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        GPIO.cleanup()
        time.sleep(shade.extended_delay)

def sendSignal(length):
    GPIO.output(TRANSMIT_PIN, 1)
    time.sleep(length)
    GPIO.output(TRANSMIT_PIN, 0)

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

if __name__ == "__main__":
    try:
        iot = createIoT()
    #rf = createRF()

    # Create your switches here, using the format:
    #   OnOff(<THING NAME>, <ON CODE>, <OFF CODE>, rf, iot)
    #
    # Example:
    #   OnOff('floor-lamp', 284099, 284108, rf, iot)
    #
    #lamps
    #OnOff('table-lamp', 1398067, 1398076, rf, iot)

    #shades family-room
    #Shades('family-room-shades', fr_ch0_off, fr_ch0_on, fr_ch0_stop, iot).set('OFF')
        #Shades('family-room-shade1', fr_ch1_off, fr_ch1_on, fr_ch1_stop, iot).set('OFF')
        #Shades('family-room-shade2', fr_ch2_off, fr_ch2_on, fr_ch2_stop, iot).set('OFF')    
        #Shades('family-room-shade3', fr_ch3_off, fr_ch3_on, fr_ch3_stop, iot).set('OFF')        
        #Shades('family-room-shade4', fr_ch4_off, fr_ch4_on, fr_ch4_stop, iot).set('OFF')

    #shades bedrooms
    #Shades('bedroom-shades', br_ch0_off, br_ch0_on, br_ch0_stop, iot).set('OFF')
        Shades('study-room-shade', sr_ch1_off, sr_ch1_on, sr_ch1_stop, iot).set('OFF')
        #Shades('aarav-room-shade', ar_ch2_off, ar_ch2_on, ar_ch2_stop, iot).set('OFF')

        print('Listening...')

        while True:
            time.sleep(0.2)
    
    except KeyboardInterrupt:
        print ('program interrupted will execute finally')

    except:
        print ('Error or exception has occured will execute finally')

    finally:
        GPIO.cleanup()
        
