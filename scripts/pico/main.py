"""
Upload this script to the pico board, then rename it to main.py.
"""

import sys
import select
from steering import Steering
from throttle import Throttle
from time import sleep

# SETUP
st = Steering(0)
th = Throttle(15)
sleep(3)  # ESC calibrate
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)
event = poller.poll()

# LOOP
while True:
    # read data from serial
    for msg, _ in event:
        buffer = msg.readline().rstrip().split(',')
        # print(buffer) # debug
        # print(len(buffer)) # debug
        if len(buffer) == 2:
            act_st, act_th = float(buffer[0]), float(buffer[1])
            # print(act_st, act_th) # debug
            st.set(act_st)
            if act_th > 0:
                th.forward(act_th)
                # print(f"FORWARD {act_th}")
            elif act_th < 0:
                th.backward(-act_th)
                # print(f"BACKWARD {act_th}")
            else:
                th.stop()
                # print("STOP")               
