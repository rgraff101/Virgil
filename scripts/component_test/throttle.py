import serial
from time import sleep


# SETUP
ser = serial.Serial('/dev/ttyACM0', 115200)

# LOOP
try:
    for i in range(1250000, 1800000, 10000): # forward up
        ser.write(bytes(f"1500000, {i}\n".encode('utf-8')))
        sleep(0.2)
    for i in reversed(range(1250000, 1800000, 10000)): # forward down
        ser.write(bytes(f"1500000, {i}\n".encode('utf-8')))
        sleep(0.2)
    for i in reversed(range(1000000, 1250000, 10000)): # reverse up
        ser.write(bytes(f"1500000, {i}\n".encode('utf-8')))
        sleep(0.2)
    for i in range(1000000, 1250000, 10000): # reverse down
        ser.write(bytes(f"1500000, {i}\n".encode('utf-8')))
        sleep(0.2)
    ser.write(bytes("1500000, 1250000\n".encode('utf-8')))
    ser.close()
except KeyboardInterrupt:
    ser.write(bytes("1500000, 1250000\n".encode('utf-8')))
    ser.close()
    print("Stopping.")
