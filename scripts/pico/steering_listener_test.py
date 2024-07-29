"""
Upload this script to the pico board, then rename it to main.py.
"""

import sys
import select
from steering import Steering
from time import sleep

# SETUP
st = Steering(16)
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)
event = poller.poll()

# LOOP
while True:
    # read data from serial
    for msg, _ in event:
        buffer = msg.readline().rstrip()
        duty = float(buffer)
        st.set(duty)
