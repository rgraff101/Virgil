"""
Transmit control signal (a float number range from -1 to 1) to Pico
Pico will decode this signal to PWM dutycycle to regulate ESC or servo
"""
import serial
from time import sleep

# SETUP
ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
print(f"Pico is connected to port: {ser.name}")

# LOOP
for i in range(100):
    msg = f"{i/100}\n".encode('utf-8')
    ser.write(msg)
    sleep(0.1)
    if ser.inWaiting() > 0:
        pico_data = ser.readline()
        pico_data = pico_data.decode('utf-8', 'ignore')
        print(pico_data)
for i in reversed(range(100)):
    msg = f"{i/100}\n".encode('utf-8')
    ser.write(msg)
    sleep(0.1)
    if ser.inWaiting() > 0:
        pico_data = ser.readline()
        pico_data = pico_data.decode('utf-8', 'ignore')
        print(pico_data)
for i in range(100):
    msg = f"{-i/100}\n".encode('utf-8')
    ser.write(msg)
    sleep(0.1)
    if ser.inWaiting() > 0:
        pico_data = ser.readline()
        pico_data = pico_data.decode('utf-8', 'ignore')
        print(pico_data)
for i in reversed(range(100)):
    msg = f"{-i/100}\n".encode('utf-8')
    ser.write(msg)
    sleep(0.1)
    if ser.inWaiting() > 0:
        pico_data = ser.readline()
        pico_data = pico_data.decode('utf-8', 'ignore')
        print(pico_data)
ser.close()
