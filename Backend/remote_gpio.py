#################################################################################
# This will be the service that handles the remote_gpio connection. It will     #
# recieve commands from the main file and relay out to the remote pi.           #
#                                                                               #
#                                                                               #
#################################################################################

from gpiozero import Robot
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

class Remote_GPIO:
    def __init__(self):
        self.run = True
        self.rem_pi = PiGPIOFactory()
        self.Jim = Robot(left=(20,21), right=(19,26))
        
    def remote_gpio_init(self):
        print("connected to pi")
        while self.run:
            print("testing forward")
            self.Jim.forward(1)
            sleep(3)
            self.Jim.stop()
            print("testing backward")
            self.Jim.backward(1)
            sleep(3)
            self.Jim.stop()
            print("testing left")
            self.Jim.left(1)
            sleep(3)
            self.Jim.stop()
            print("testing right")
            self.Jim.right(1)
            sleep(3)
            self.Jim.stop()
            print("finished tests")
            self.close_connection()

    def left(self, value):
        print("going left @: " + str(value))
        self.Jim.left(value)
        
    def forward(self, value):
        print("going forward @: " + str(value))
        self.Jim.forward(value)
        
    def backward(self, value):
        print("going backward @: " + str(value))
        self.Jim.backward(value)
        
    def right(self, value):
        print("going right @: " + str(value))
        self.Jim.right(value)

    def process_input(self, value, mag):
        print("Heading: " + value + " @: " + str(mag))
        self.Jim.value(mag)
        
    
    def close_connection(self):
        self.run = False
