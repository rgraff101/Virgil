"""
Upload this script to the pico board, then rename it to main.py.
"""
import sys
import select
from throttle import Throttle

# SETUP
th = Throttle(15)
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)
event = poller.poll()

# LOOP
while True:
    # read data from serial
    for msg, _ in event:
        buffer = msg.readline().rstrip()
        throttle_duty = int(buffer)
        th.forward(throttle_duty)
