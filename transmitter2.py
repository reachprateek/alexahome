import time
import sys
import RPi.GPIO as GPIO

#family room
fr_ch0_up = '0100100000110001111100110101000000011110'
fr_ch0_down = '0100100000110001111100110101000000111100'
fr_ch0_stop = '0100100000110001111100110101000001010101'


fr_ch1_up = '0100100000110001111100110101000100011110'
fr_ch1_down = '0100100000110001111100110101000100111100'
fr_ch1_stop = '0100100000110001111100110101000101010101'


fr_ch2_up = '0100100000110001111100110101001000011110'
fr_ch2_down = '0100100000110001111100110101001000111100'
fr_ch2_stop = '0100100000110001111100110101001001010101'


fr_ch3_up = '0100100000110001111100110101001100011110'
fr_ch3_down = '0100100000110001111100110101001100111100'
fr_ch3_stop = '0100100000110001111100110101001101010101'


fr_ch4_up = '0100100000110001111100110101010000011110'
fr_ch4_down = '0100100000110001111100110101010000110011'
fr_ch4_stop = '0100100000110001111100110101010001010101'

#study room
sr_ch1_up = '1101000000110001001101110010000100010001'
sr_ch1_down = '1101000000110001001101110010000100110011'
sr_ch1_stop = '1101000000110001001101110010000101010101'

ar_ch2_up = '1101000000110001001101110010001000010001'
ar_ch2_down = '1101000000110001001101110010001000110011'
ar_ch2_stop = '1101000000110001001101110010001001010101'


NUM_ATTEMPTS = 10
TRANSMIT_PIN = 17


class Shades:

    starter = 0.0047
    time_to_first_bit_delay = 0.0015
    zero = 0.00028
    one = 0.00062
    after_zero_delay = 0.0008
    after_one_delay = 0.00045
    extended_delay = 0.01

    def __init__(self, name, upCode, downCode, stopCode, gpio):
        self.name = name
        self.upCode = upCode
        self.downCode = downCode
        self.stopCode = stopCode
        self.gpio = gpio
        self.set('DOWN')

    def set(self, state):
        choices = {'UP': self.upCode, 'DOWN': self.downCode, 'STOP': self.stopCode}
        code = choices.get(state, self.stopCode)
        print('Turning %s %s using code %s' % (self.name, state, code))
        self.transmit_code(code)

    def transmit_code(self, code):
        for t in range(NUM_ATTEMPTS):
            self.sendSignal(self.gpio, self.starter)
            time.sleep(self.time_to_first_bit_delay)
            for i in code:
                if i == '0':
                    self.sendSignal(self.gpio, self.zero)
                    time.sleep(self.after_zero_delay)
                elif i == '1':
                    self.sendSignal(self.gpio, self.one)
                    time.sleep(self.after_one_delay)
                else:
                    continue
        self.gpio.cleanup()

    def sendSignal(self, gpio, length):
        gpio.output(TRANSMIT_PIN, 1)
        time.sleep(length)
        gpio.output(TRANSMIT_PIN, 0)        

def createGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    return GPIO
   
 
if __name__ == '__main__':
    gpio = createGPIO()
    Shades('study-room-shade', sr_ch1_up, sr_ch1_down, sr_ch1_stop, gpio)
