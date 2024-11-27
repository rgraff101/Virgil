import sys
import os
import json
from time import time
from datetime import datetime
import csv
import serial
import pygame
import cv2 as cv
from picamera2 import Picamera2
from gpiozero import LED

# SETUP
# Load configs
params_file_path = os.path.join(sys.path[0], 'configs.json')
with open(params_file_path) as params_file:
    params = json.load(params_file)

# Constants
THROTTLE_AXIS = params['throttle_joy_axis']  # Axis for forward/backward
STEERING_AXIS = params['steering_joy_axis']  # Axis for left/right
THROTTLE_STALL = params['throttle_stall']
THROTTLE_FWD_RANGE = params['throttle_fwd_range']
THROTTLE_REV_RANGE = params['throttle_rev_range']
THROTTLE_LIMIT = params['throttle_limit']
RECORD_BUTTON = params['record_btn']
STOP_BUTTON = params['stop_btn']

# Init LED
headlight = LED(params['led_pin'])
headlight.off()

# Init serial port
ser_pico = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
print(f"Pico is connected to port: {ser_pico.name}")

# Init controller
pygame.display.init()
pygame.joystick.init()
try:
    js = pygame.joystick.Joystick(0)
except pygame.error:
    print("No joystick found!")
    sys.exit()

# Create data directory
image_dir = os.path.join(
    os.path.dirname(sys.path[0]),
    'data', datetime.now().strftime("%Y-%m-%d-%H-%M"),
    'images/'
)
os.makedirs(image_dir, exist_ok=True)
label_path = os.path.join(os.path.dirname(os.path.dirname(image_dir)), 'labels.csv')

# Init camera
cv.startWindowThread()
cam = Picamera2()
cam.configure(
    cam.create_preview_configuration(
        main={"format": 'RGB888', "size": (640, 640)}
    )
)
cam.start()

# Debugging: ensure the camera is ready
print("Camera started. Testing frame capture...")
for i in range(10):
    frame = cam.capture_array()
    if frame is not None:
        print(f"DEBUG: Frame received with shape {frame.shape}")
    else:
        print("DEBUG: Frame is None!")
        sys.exit("No frames captured. Check camera setup.")

# Init timer for FPS computing
start_stamp = time()
frame_counts = 0

# Init variables
ax_val_th = 0.0  # Shut throttle
ax_val_st = 0.0  # Center steering
is_recording = False

# Commands
COMMANDS = {
    "FORWARD": "FORWARD,50\n",
    "BACKWARD": "BACKWARD,50\n",
    "LEFT": "LEFT,50\n",
    "RIGHT": "RIGHT,50\n",
    "STOP": "STOP\n"
}

# LOOP
try:
    while True:
        frame = cam.capture_array()  # Read image
        if frame is None:
            print("DEBUG: Frame is None!")
            continue  # Skip this iteration if no frame

        # Show the camera feed for debugging
        cv.imshow("Camera Preview", frame)
        cv.waitKey(1)  # Refresh the OpenCV window

        for e in pygame.event.get():  # Read controller input
            if e.type == pygame.JOYAXISMOTION:
                ax_val_th = round(js.get_axis(THROTTLE_AXIS), 2)  # Throttle axis (up/down)
                ax_val_st = round(js.get_axis(STEERING_AXIS), 2)  # Steering axis (left/right)
            elif e.type == pygame.JOYBUTTONDOWN:
                if js.get_button(RECORD_BUTTON):
                    is_recording = not is_recording
                    print(f"Recording: {is_recording}")
                    headlight.toggle()
                elif js.get_button(STOP_BUTTON):  # Emergency stop
                    print("E-STOP PRESSED. TERMINATE!")
                    headlight.off()
                    headlight.close()
                    cv.destroyAllWindows()
                    pygame.quit()
                    ser_pico.close()
                    sys.exit()

        # Calculate throttle values
        act_th = -ax_val_th  # Throttle action: -1: max forward, 1: max backward

        # Determine forward/backward command
        if act_th > 0:
            ser_pico.write(COMMANDS["FORWARD"].encode('utf-8'))
        elif act_th < 0:
            ser_pico.write(COMMANDS["BACKWARD"].encode('utf-8'))
        else:
            ser_pico.write(COMMANDS["STOP"].encode('utf-8'))

        # Determine left/right steering command
        if ax_val_st > 0.5:
            ser_pico.write(COMMANDS["RIGHT"].encode('utf-8'))
        elif ax_val_st < -0.5:
            ser_pico.write(COMMANDS["LEFT"].encode('utf-8'))
        else:
            ser_pico.write(COMMANDS["STOP"].encode('utf-8'))

        # Log data
        action = [act_th, ax_val_st]
        if is_recording:
            cv.imwrite(image_dir + str(frame_counts) + '.jpg', frame)
            label = [str(frame_counts) + '.jpg'] + action
            with open(label_path, 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(label)

        frame_counts += 1
        # Log frame rate
        since_start = time() - start_stamp
        frame_rate = frame_counts / since_start
        print(f"frame rate: {frame_rate}")

except Exception as e:
    print(f"An error occurred: {e}")
    headlight.off()
    headlight.close()
    cv.destroyAllWindows()
    pygame.quit()
    ser_pico.close()
    sys.exit("Program terminated.")
