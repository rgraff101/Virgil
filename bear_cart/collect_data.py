import sys
import os
from datetime import datetime
import cv2 as cv
from picamera2 import Picamera2
import pygame
from gpiozero import AngularServo, PhaseEnableMotor
import json
from time import time
import csv


# SETUP
# Load configs
params_file_path = os.path.join(sys.path[0], 'configs.json')
params_file = open(params_file_path)
params = json.load(params_file)
# Constants
STEER_AXIS = params['steer_joy_axis']
THROTTLE_AXIS = params['throttle_joy_axis']
RECORD_BUTTON = params['record_btn']
STOP_BUTTON = params['stop_btn']
STEER_CENTER = params['steer_center_angle']
STEER_RANGE = params['steer_range']
STEER_DIR = params['steer_dir']
THROTTLE_LIMIT = params['throttle_limit']
# Init servo 
steer = AngularServo(
    pin=params['steer_pin'], 
    initial_angle=params['steer_center_angle'], 
    min_angle=params['steer_min_angle'], 
    max_angle=params['steer_max_angle'],
)
# Init motor 
throttle = PhaseEnableMotor(
    phase=params['throttle_dir_pin'], 
    enable=params['throttle_pwm_pin'],
)
# Init controller
pygame.display.init()
pygame.joystick.init()
js = pygame.joystick.Joystick(0)
# Create data directory
image_dir = os.path.join(sys.path[0], 'data', datetime.now().strftime("%Y_%m_%d_%H_%M"), 'images/')
if not os.path.exists(image_dir):
    try:
        os.makedirs(image_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
label_path = os.path.join(os.path.dirname(os.path.dirname(image_dir)), 'labels.csv')
# Init camera
cam = Picamera2()
cam.configure(
    cam.create_preview_configuration(
        main={"format": 'RGB888', "size": (120, 160)},
        controls={"FrameDurationLimits": (50000, 50000)},  # 20 FPS
    )
)
cam.start()
for i in reversed(range(60)):
    frame = cam.capture_array()
    # cv.imshow("Camera", frame)
    # cv.waitKey(1)
    if frame is None:
        print("No frame received. TERMINATE!")
        sys.exit()
    if not i % 20:
        print(i/20)  # count down 3, 2, 1 sec
# Init timer for FPS computing
start_stamp = time()
frame_counts = 0
ave_frame_rate = 0.
# Init joystick axes values
st_ax_val, th_ax_val = 0., 0.
is_recording = False

# MAIN LOOP
try:
    while True:
        frame = cam.capture_array()  # read image
        if frame is None:
            print("No frame received. TERMINATE!")
            sys.exit()
        for e in pygame.event.get():  # read controller input
            if e.type == pygame.JOYAXISMOTION:
                st_ax_val = round((js.get_axis(STEER_AXIS)), 2)  
                th_ax_val = round((js.get_axis(THROTTLE_AXIS)), 2)  # keep 2 decimals
            elif e.type == pygame.JOYBUTTONDOWN:
                if js.get_button(STOP_BUTTON):  # emergency stop 
                    throttle.stop()
                    throttle.close()
                    steer.close()
                    cv.destroyAllWindows()
                    pygame.quit()
                    print("E-STOP PRESSED. TERMINATE")
                    sys.exit()
                elif js.get_button(RECORD_BUTTON):
                    is_recording = not is_recording
                    print(f"Recording: {is_recording}")
        # Calaculate steering and throttle value
        act_st = st_ax_val  # steer action: -1: left, 1: right
        act_th = -th_ax_val  # throttle action: -1: max forward, 1: max backward
        # Drive servo
        steer.angle = STEER_CENTER + act_st * STEER_RANGE * STEER_DIR
        # Drive motor
        if act_th >= 0.1:
            throttle.forward(min(act_th, THROTTLE_LIMIT))
        elif act_th <= -0.1:
            throttle.backward(min(-act_th, THROTTLE_LIMIT))
        else:
            throttle.stop()
        # Log data
        action = [act_st, act_th]
        print(f"action: {action}")
        if is_recording:
            # img = cv.resize(frame, (120, 160))
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
        # Press "q" to quit
        if cv.waitKey(1)==ord('q'):
            throttle.stop()
            throttle.close()
            steer.close()
            cv.destroyAllWindows()
            pygame.quit()
            sys.exit()
            
# Take care terminate signal (Ctrl-c)
except KeyboardInterrupt:
    throttle.stop()
    throttle.close()
    steer.close()
    cv.destroyAllWindows()
    pygame.quit()
    sys.exit()