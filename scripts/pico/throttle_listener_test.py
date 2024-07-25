"""
Upload this script to the pico board, then rename it to main.py.
"""

import sys
import select
from throttle import Throttle
from time import sleep

# SETUP
th = Throttle(15)
sleep(3)  # ESC calibrate
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)
event = poller.poll()

# LOOP
while True:
    # read data from serial
    for msg, _ in event:
        buffer = msg.readline().rstrip()
        throttle_duty = float(buffer)
        if throttle_duty > 0:
            th.forward(throttle_duty)
            print("FORWARD")
        elif throttle_duty < 0:
            th.backward(throttle_duty)
            print("BACKWARD")
        else:
            th.stop()
            print("STOP")
