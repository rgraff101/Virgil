"""
Upload this script to the pico board, then rename it to main.py.
"""
import sys
import select
from engine import Engine

# SETUP
motor = Engine(15)
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)
event = poller.poll()

# LOOP
while True:
    # read data from serial
    for msg, _ in event:
        buffer = msg.readline().rstrip()
        if len(buffer) == 2:
            motor_duty = int(buffer)
            motor.forward(motor_duty)
