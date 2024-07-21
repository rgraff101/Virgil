import sys
import os
from gpiozero import LED
from time import sleep
import json

# Load configs
params_file_path = os.path.join(os.path.dirname(sys.path[0]), 'configs.json')
params_file = open(params_file_path)
params = json.load(params_file)

# SETUP
led = LED(params['led_pin'])

for _ in range(10):
    led.on()
    sleep(1)
    led.off()
    sleep(1)
