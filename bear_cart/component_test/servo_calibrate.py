"""
Start with initial_angle=0, min_angle=-90, max_angle=90
Observe and log calibrated angle values below:
    left most angle: -30
    right most angle: 90
    center: 30
Hint: running in Python's interactive mode
"""
from gpiozero import AngularServo
from time import sleep

servo = AngularServo(12, initial_angle=30, min_angle=-90, max_angle=90)

for ang in range(-30, 90, 5):
    servo.angle = ang
    print(ang)
    sleep(.5)

servo.angle = 30
print("CENTER")
sleep(1)
