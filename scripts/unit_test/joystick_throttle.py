"""
Integrated test with controller, pico usb communication, throttle motor.
"""
import sys
import os
import serial
import pygame
import json
from time import sleep


# SETUP
# Load configs
params_file_path = os.path.join(os.path.dirname(sys.path[0]), 'configs.json')
params_file = open(params_file_path)
params = json.load(params_file)
# Constants
THROTTLE_AXIS = params['throttle_joy_axis']
STOP_BUTTON = params['stop_btn']
# THROTTLE_LIMIT = params['throttle_limit']
THROTTLE_LIMIT = 99
# Init serial port 
ser_pico = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
print(f"Connection to port {ser_pico.name} established.")
# Init controller
pygame.display.init()
pygame.joystick.init()
js = pygame.joystick.Joystick(0)
# Init joystick axes values
th_ax_val = 0.

# MAIN LOOP
try:
    while True:
        for e in pygame.event.get():  # read controller input
            if e.type == pygame.JOYAXISMOTION:
                th_ax_val = round((js.get_axis(THROTTLE_AXIS)), 2)  # keep 2 decimals
            elif e.type == pygame.JOYBUTTONDOWN:
                if js.get_button(STOP_BUTTON):  # emergency stop 
                    print("E-STOP PRESSED. TERMINATE")
                    pygame.quit()
                    ser_pico.close()
                    sys.exit()
        # Calaculate steering and throttle value
        act_th = -th_ax_val  # throttle action: -1: max forward, 1: max backward
        # Drive motor
        msg = f"{act_th}\n".encode('utf-8')
        ser_pico.write(msg)
        # Log action
        print(f"throttle value: {act_th}")
        # 20Hz
        sleep(0.05)

# Take care terminal signal (Ctrl-c)
except KeyboardInterrupt:
    pygame.quit()
    ser_pico.close()
    sys.exit()
