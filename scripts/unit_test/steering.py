import serial
from time import sleep


# SETUP
ser = serial.Serial('/dev/ttyACM0', 115200)

# LOOP
try:
    for i in range(1000000, 2000000, 10000):
        ser.write(bytes(f"{i}, 1250000\n".encode('utf-8')))
        sleep(0.2)
    for i in reversed(range(1000000, 2000000, 10000)):
        ser.write(bytes(f"{i}, 1250000\n".encode('utf-8')))
        sleep(0.2)
    ser.write(bytes("1500000, 1250000\n".encode('utf-8')))
    ser.close()
except KeyboardInterrupt:
    ser.write(bytes("1500000, 1250000\n".encode('utf-8')))
    ser.close()
    print("Stopping.")
