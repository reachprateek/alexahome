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


shades_starter_code = 0.0047
shades_time_to_first_bit_delay = 0.0015
shades_zero = 0.00028
shades_one = 0.00062
shades_after_zero_delay = 0.0008
shades_after_one_delay = 0.00045
shades_extended_delay = 0.01

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 17

def transmit_code(gpio, code):
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    '''Transmit a chosen code string using the GPIO transmitter'''
    print("Sending code ", code)
    for t in range(NUM_ATTEMPTS):
        sendSignal(gpio, shades_starter_code)
        time.sleep(shades_time_to_first_bit_delay)
        for i in code:
            if i == '0':
                sendSignal(gpio, shades_zero)
                time.sleep(shades_after_zero_delay)
            elif i == '1':
                sendSignal(gpio, shades_one)
                time.sleep(shades_after_one_delay)
            else:
                continue
        gpio.output(TRANSMIT_PIN, 0)
        time.sleep(shades_extended_delay)
    GPIO.cleanup()

def sendSignal(gpio, length):
    gpio.output(TRANSMIT_PIN, 1)
    time.sleep(length)
    gpio.output(TRANSMIT_PIN, 0)

def createGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    return GPIO    
    
if __name__ == '__main__':

    gpio = createGPIO()
    for argument in sys.argv[1:]:
        exec('transmit_code(gpio,' + str(argument) + ')')
