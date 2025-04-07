#  Code for the Grove ultrasonic sensor - this code uses trigger and echo on
#  the same pins which is called a Ping Sensor.  This is based on the general version 
#  which will work with the common ultrasonic sensor used with the ardino - HCSR0
#  sensor adopted from source =
# https://github.com/shaoziyang/microbit-lib/tree/master/sensor/HCSR04
#  The ping))) sensor from grove pi uses a single pin
#  if the trigger and echo pin are the same the the basic
#  microbit operations will work
#
# Author: S Brophy
# Date: October 2020  -  Version 1: Original

from microbit import *
from time import sleep_us
from machine import time_pulse_us

TIME_OUT = 100000  # Increase time out to see farther, but
# this will reduce the sample rate
ECHO = pin1      # ping sensor uses a single pin for ECHO and Trigger
TRIGGER = pin1

def distance(tp, ep):
    # tp is the trigger pin and ep is the echo pin
    ep.read_digital()  # clear echo
    tp.write_digital(1)  # Send a 10 microSec pulse
    sleep_us(10)  # wait 10 microSec
    tp.write_digital(0)  # Send pulse low
    ep.read_digital()  # clear echo signal - This is needed for a
    # pingSensor
    ts = time_pulse_us(ep, 1, TIME_OUT)  # Wait for echo or time out
    if ts > 0:
        ts = ts * 17 // 100  # if system did not timeout, then send
        # back a scaled value
    return ts  # Return timeout error as a negative number (-1)


def main():
    display.show("U")     #provide feedback that Ping sensor is running
    while True:
        dist = distance(TRIGGER, ECHO)  # set up to read as a ping)))
        # sensor same pin
        print(dist)    # use serial terminal to get information
        sleep(500)     # set for a slow update rate


if __name__ == "__main__":
    main()
