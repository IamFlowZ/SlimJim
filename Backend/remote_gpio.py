#################################################################################
# This will be the service that handles the remote_gpio connection. It will     #
# recieve commands from the main file and relay out to the remote pi.           #
#                                                                               #
#                                                                               #
#################################################################################

from gpiozero import PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

class Remote_GPIO:
    def __init__(self):
        self.run = True
        self.rem_pi = PiGPIOFactory()
        self.led_green = PWMLED(26)
        self.led_blue = PWMLED(14)
        self.led_yellow = PWMLED(15)
        self.led_red = PWMLED(18)
        
    def remote_gpio_init(self):
        print("connected to pi")
        while self.run:
            print("turning on leds")
            self.led_green.pulse()
            self.led_blue.pulse()
            self.led_yellow.pulse()
            self.led_red.pulse()
            sleep(1)
            print("turning off leds")
            #led.off()
            self.led_green.off()
            self.led_blue.off()
            self.led_yellow.off()
            self.led_red.off()
            sleep(1)
            self.close_connection()

    def left(self, value):
        self.led_green.value = value
        print("green led @: " + str(value))
        self.led_green.toggle()
        sleep(1)
        self.led_green.off()
        
    def forward(self, value):
        self.led_blue.value = value
        print("blue led @: " + str(value))
        self.led_blue.toggle()
        sleep(1)
        self.led_blue.off()
        
    def backward(self, value):
        self.led_yellow.value = value
        print("yellow led @: " + str(value))
        self.led_yellow.toggle()
        sleep(1)
        self.led_yellow.off()
        
    def right(self, value):
        self.led_red.value = value
        print("red led @: " + str(value))
        self.led_red.toggle()
        sleep(1)
        self.led_red.off()
        
    def close_connection(self):
        self.run = False
