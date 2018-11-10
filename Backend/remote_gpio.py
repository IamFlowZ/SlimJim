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
        
    
    def close_connection(self):
        self.run = False
