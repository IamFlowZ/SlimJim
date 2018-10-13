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
        self.Jim = Robot(left=(2,3), right=(20,21))
        
    def remote_gpio_init(self):
        print("connected to pi")
        while self.run:
            print("testing forward")
            self.Jim.forward()
            sleep(1)
            self.Jim.stop()
            print("testing backward")
            self.Jim.backward()
            sleep(1)
            self.Jim.stop()
            print("testing left")
            self.Jim.left()
            sleep(1)
            self.Jim.stop()
            print("testing right")
            self.Jim.right()
            sleep(1)
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
        
    def close_connection(self):
        self.run = False
