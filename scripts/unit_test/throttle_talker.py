import serial
from time import sleep

# SETUP
ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
print(ser.name)

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
