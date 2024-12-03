from picodebug import Motor
from time import sleep_ms

# SETUP - Initialize motors
left_motor = Motor(3, 2, 14, 15, 4)  # Left motor pins
right_motor = Motor(7, 6, 12, 13, 8)  # Right motor pins

# Enable the motors
left_motor.enable()
right_motor.enable()

# Main loop - Listen for commands
# print("Listening for commands...")  # Commented out to suppress output
buffer = ""
while True:
    try:
        buffer += input()  # Add input to buffer

        if '\n' in buffer:  # Process complete commands
            commands = buffer.split('\n')
            buffer = commands[-1]  # Retain incomplete command, if any
            
            # Loop through each complete command
            for command in commands[:-1]:
                # print(f"Received command: {command.strip()}")  # Commented out to suppress output
                try:
                    parts = command.split(',')
                    cmd = parts[0]
                    # print(f"Processing command: {cmd}")  # Commented out to suppress output

                    if cmd == "FORWARD":
                        left_speed = int(parts[1]) / 100  # Scale speed to 0-1
                        right_speed = int(parts[2]) / 100
                        left_motor.forward(left_speed)
                        right_motor.forward(right_speed)
                        # print(f"Moving forward: L={left_speed}, R={right_speed}")  # Commented out to suppress output
                    elif cmd == "BACKWARD":
                        left_speed = int(parts[1]) / 100
                        right_speed = int(parts[2]) / 100
                        left_motor.backward(left_speed)
                        right_motor.backward(right_speed)
                        # print(f"Moving backward: L={left_speed}, R={right_speed}")  # Commented out to suppress output
                    elif cmd == "STOP":
                        left_motor.stop()
                        right_motor.stop()
                        # print("Motors stopped")  # Commented out to suppress output
                    else:
                        # print(f"Unknown command: {cmd}")  # Commented out to suppress output
                        pass
                except (ValueError, IndexError) as e:
                    # print(f"Error processing command: {command} - {e}")  # Commented out to suppress output
                    pass
    except KeyboardInterrupt:
        # print("\nExiting listener.")  # Commented out to suppress output
        left_motor.stop()
        right_motor.stop()
        left_motor.disable()
        right_motor.disable()
        break
    sleep_ms(10)

