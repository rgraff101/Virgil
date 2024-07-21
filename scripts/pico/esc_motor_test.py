from machine import Pin, PWM
from time import sleep

# SETUP
motor = PWM(Pin(15))
motor.freq(50)

# LOOP
for i in range(1250000, 1800000, 10000): # forward up
    motor.duty_ns(i)
    print(i)
    sleep(0.2)
for i in reversed(range(1250000, 1800000, 10000)): # forward down
    motor.duty_ns(i)
    print(i)
    sleep(0.2)
for i in reversed(range(1000000, 1250000, 10000)): # reverse up
    motor.duty_ns(i)
    print(i)
    sleep(0.2)
for i in range(1000000, 1250000, 10000): # reverse down
    motor.duty_ns(i)
    print(i)
    sleep(0.2)
motor.duty_ns(1250000)


