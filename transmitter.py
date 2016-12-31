import time
import sys
import RPi.GPIO as GPIO


#ch1_on = '0100100000110001111100110101000100010001'
#ch1_on = '0100100000110001111100110101000100011110'
fr_ch1_on = '0100100000110001111100110101000100011110'
sr_ch1_up = '1101000000110001001101110010000100010001'
sr_ch1_down = '1101000000110001001101110010000100110011'
sr_ch1_stop = '1101000000110001001101110010000101010101'

starter_code_delay = 0.0047
time_to_first_bit_delay = 0.0015
short_delay = 0.00028
long_delay = 0.00062
zero_to_delay = 0.0008
one_to_delay = 0.00045
extended_delay = 0.01

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 17
#TRANSMIT_PIN = 2

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    print("Sending code ", code)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        GPIO.output(TRANSMIT_PIN, 1)
        time.sleep(starter_code_delay)
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(time_to_first_bit_delay)
        for i in code:
            if i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(zero_to_delay)
            elif i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(long_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(one_to_delay)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(extended_delay)
    GPIO.cleanup()

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')

