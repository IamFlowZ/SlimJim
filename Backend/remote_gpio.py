#################################################################################
# This will be the service that handles the remote_gpio connection. It will     #
# recieve commands from the main file and relay out to the remote pi.           #
#                                                                               #
#                                                                               #
#################################################################################

from gpiozero import Motor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

class Remote_GPIO:
    def __init__(self):
        self.run = True
        self.rem_pi = PiGPIOFactory()
        self.motor_left = Motor(20,21)
        self.motor_right = Motor(19,26)

        
    def remote_gpio_init(self):
        print("connected to pi")
        while self.run:
            print("testing forward")
            self.motor_left.forward()
            self.motor_right.forward()
            sleep(2)
            self.motor_right.stop()
            self.motor_left.stop()
            print("testing backward")
            self.motor_left.backward()
            self.motor_right.backward()
            sleep(2)
            self.motor_right.stop()
            self.motor_left.stop()
            print("testing left")
            self.motor_left.forward()
            sleep(2)
            self.motor_left.stop()
            print("testing right")
            self.motor_right.forward()
            sleep(2)
            self.motor_right.stop()
            print("finished tests")
            self.motor_left.stop()
            self.motor_right.stop()
            self.close_connection()

    # Passing zero means turning it off, Passing one is full on.
    def left(self, value):
        print("going left @: " + str(value))
        
        
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
