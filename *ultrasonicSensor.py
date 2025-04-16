# The micro:bit sensor code is used to connect to the Spyder GUI app.

from microbit import *
from time import sleep_us
from machine import time_pulse_us
import radio

# Constants
TIME_OUT = 100000      # Timeout for the echo pulse
TRIGGER1 = pin1        # the pin for the first sensor
TRIGGER2 = pin2        # the pin for the second sensor
ECHO1 = pin1
ECHO2 = pin2

chnl = 3     # channel to connect to other microbit
radio.config(channel=chnl)
radio.on()

MIN_DISTANCE = 2      # x: minimum distance to detect object
MAX_DISTANCE = 40      # y: maximum distance to detect object

def distance(tp, ep):
    ep.read_digital()       # Clear echo
    tp.write_digital(1)     # Send pulse out
    sleep_us(10)
    tp.write_digital(0)
    ep.read_digital()       

    ts = time_pulse_us(ep, 1, TIME_OUT)
    if ts > 0:
        ts = ts * 17 // 100  # Convert to cm
    return ts  # Return -1 if timeout error

def main():
    display.show("U")  # Show that the ultrasonic sensor is running
    while True:
        dist1 = distance(TRIGGER1, ECHO1)
        dist2 = distance(TRIGGER2, ECHO2)
        left = 1    # if the left spot is available
        right = 1    # if the right spot is available
        spaces = 0   # will count the spaces available
        if dist1 > 0 and MIN_DISTANCE <= dist1 <= MAX_DISTANCE:
            left -= 1    # object is detected 
        else:
            spaces += 1    # no object is detected
        sleep(500)
        if dist2 > 0 and MIN_DISTANCE <= dist2 <= MAX_DISTANCE:
            right -= 1    # object is detected
        else:
            spaces += 1    # no object is detected
        sleep(500)
        display.show(spaces)    # displays amount of spaces open
      
        # checks if the left and right spots are open and sends to the Python app
        if left == 1 and right == 1:  
            print("O") 
        elif left == 1 and right == 0:
            print("L")   
        elif left == 0 and right == 1:
            print("R")   
        else:
            print("X")  

if __name__ == "__main__":
    main()
