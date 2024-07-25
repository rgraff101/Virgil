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
        duty = float(buffer)
        if duty > 0:
            th.forward(duty)
            print(f"FORWARD {duty}")
        elif duty < 0:
            th.backward(duty)
            print(f"BACKWARD {duty}")
        else:
            th.stop()
            print("STOP")
