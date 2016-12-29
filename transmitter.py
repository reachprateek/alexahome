import time
import sys
import RPi.GPIO as GPIO

#a_on = '1111111111111010101011101'
#a_on = '0001010101010101001100110'
#a_off = '0001010101010101001111000'

#a_on = '1110101010101010110011001'
#a_off = '1111111111111010101010111'
#b_on = '1111111111101110101011101'
#b_off = '1111111111101110101010111'
#c_on = '1111111111101011101011101'
#c_off = '1111111111101011101010111'
#d_on = '1111111111101010111011101'
#d_off = '1111111111101010111010111'

ch1_on = '0100100000110001111100110101000100010001'

short_delay = 0.00050
long_delay = 0.00085
extended_delay = 0.01

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 17

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    print("Sending code ", code)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        for i in code:
            if i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(long_delay)
            elif i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(long_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(short_delay)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(extended_delay)
    GPIO.cleanup()

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')

