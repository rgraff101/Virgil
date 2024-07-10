"""
Start with initial_angle=0, min_angle=-90, max_angle=90
Observe and log calibrated angle values below:
    left most angle: 
    right most angle: 
    center: 30
Hint: running in Python's interactive mode
"""
import sys
import os
from gpiozero import AngularServo
from time import sleep
import json

# Load configs
params_file_path = os.path.join(os.path.dirname(sys.path[0]), 'configs.json')
params_file = open(params_file_path)
params = json.load(params_file)

# SETUP
print("Please take down the angle values when front wheels are turned all the to the left, right and centered.")
for i in reversed(range(1, 4)):
    print(i)
    sleep(1)
servo = AngularServo(
    pin=params['steer_pin'], 
    initial_angle=params['steer_center_angle'], 
    min_angle=params['steer_min_angle'], 
    max_angle=params['steer_max_angle'],
)

# LOOP
for ang in range(-90, 90, 5):
    servo.angle = ang
    print(ang)
    sleep(.5)

servo.angle = 30
print("CENTER")
sleep(1)
