import serial
from time import sleep

# SETUP
ser = serial.Serial(port='/dev/ttyACM0', baudrate=19200)
print(ser.name)

# LOOP
for i in range(10):
    ser.write(b"Hello from RPi")
    print('Transmitting "Hello from RPi"')
    sleep(1)
ser.close()
