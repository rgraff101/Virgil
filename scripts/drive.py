"""
Integrated test with controller, Pico USB communication, and differential steering.
"""
import sys
import os
import serial
import pygame
import json
from time import sleep

# SETUP
# Load configs
params_file_path = '/home/virgil/Virgil/scripts/configs.json'
with open(params_file_path) as params_file:
    params = json.load(params_file)

# Constants
THROTTLE_AXIS = params['throttle_joy_axis']
STEERING_AXIS = params['steering_joy_axis']
THROTTLE_LIMIT = params['throttle_limit']
STOP_BUTTON = params['stop_btn']

# Init serial port
ser_pico = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
print(f"Pico is connected to port: {ser_pico.name}")

# Init controller
pygame.display.init()
pygame.joystick.init()
try:
    js = pygame.joystick.Joystick(0)
    js.init()
    print(f"Controller initialized: {js.get_name()}")
except pygame.error as e:
    print(f"No joystick found: {e}")
    sys.exit()

# Init joystick axes values
ax_val_th = 0.0
ax_val_st = 0.0

# MAIN LOOP
try:
    while True:
        # Read controller input
        for e in pygame.event.get():
            if e.type == pygame.JOYAXISMOTION:
                ax_val_th = round(js.get_axis(THROTTLE_AXIS), 2)  # Throttle axis (forward/backward)
                ax_val_st = round(js.get_axis(STEERING_AXIS), 2)  # Steering axis (left/right)
            elif e.type == pygame.JOYBUTTONDOWN:
                if js.get_button(STOP_BUTTON):  # Emergency stop
                    print("E-STOP PRESSED. TERMINATING!")
                    ser_pico.write(b"STOP\n")
                    pygame.quit()
                    ser_pico.close()
                    sys.exit()

        # Throttle calculation
        act_th = -ax_val_th  # Invert throttle: -1 = max forward, 1 = max backward
        throttle_speed = int(abs(act_th) * 100)  # Scale to 0-100

        # Differential steering logic
        if ax_val_st > 0:  # Turning right
            left_speed = throttle_speed  # Left wheel moves forward
            right_speed = int(throttle_speed * (1 - ax_val_st))  # Scale down right wheel
        elif ax_val_st < 0:  # Turning left
            right_speed = throttle_speed  # Right wheel moves forward
            left_speed = int(throttle_speed * (1 + ax_val_st))  # Scale down left wheel
        else:  # Going straight
            left_speed = right_speed = throttle_speed

        # Direction determination
        if act_th > 0:  # Forward
            command = f"FORWARD,{left_speed},{right_speed}\n"
        elif act_th < 0:  # Backward
            command = f"BACKWARD,{left_speed},{right_speed}\n"
        else:  # Stop
            command = "STOP\n"

        # Send command to Pico
        ser_pico.write(f"{command.strip()}\n".encode('utf-8'))

        # Log actions for debugging
        print(f"Throttle: {act_th}, Steering: {ax_val_st}, Command: {command.strip()}")

        # Maintain loop rate at 20Hz
        sleep(0.05)

except KeyboardInterrupt:
    print("Exiting gracefully...")
    pygame.quit()
    ser_pico.close()
    sys.exit()

