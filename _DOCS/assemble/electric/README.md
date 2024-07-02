# Electronic Components Wiring Guide
![wiring-all](/_DOCS/assemble/electric/images/wiring-all.jpg)

It is recommended to follow the order as stated below to wire up the electric components.

## 1 Split Battery Power
The LiPo battery will provide power for all the electric components. 
So, split the power and employ a rocker switch for the convenience of cutting off the power.

**Color coding the positive and negative power lines is extremely recommended.**

![battery-switch-splitter](/_DOCS/assemble/electric/images/battery-switch-splitter.jpg)

## 2 Powering Up Steering Servo
A 3-wire servo motor is responsible for turning the front wheels of the BearCart.
There are two widely used color codes for the servo wires.
Please refer to the following table for details:
![servo_color](https://i0.wp.com/dronebotworkshop.com/wp-content/uploads/2018/05/servo-motor-pinout.jpg?w=768&ssl=1)

Most hobby servos are rated from 4.8 to 6 volts.
We convert the battery power to 5 volts to feed the need of the servo motor. 
![splitter-buck-servo](/_DOCS/assemble/electric/images/splitter-buck-servo.jpg)

## 3 Powering Up Motor Driver
**Pay attention to the polarity of the power port (labeled with "+" and "-")**

![splitter-md-motor](/_DOCS/assemble/electric/images/splitter-md-motor.jpg)

## 4 Powering Up Raspberry Pi
- A Raspberry Pi can be powered up from a '5V' (positive) and a 'GND' (negative) pin among the GPIO pins.
- **Apply a power source over 5 volts may damage the Raspberry Pi.**
![splitter-buck-rpi](/_DOCS/assemble/electric/images/splitter-buck-rpi5.jpg)

## 5 GPIO Wiring
- Raspberry Pi is in charge of controlling the steering servo and thrust motor.
- The control signals are handled by some of the GPIO pins.
- The GPIO pins employed as shown in the diagram below are the default setting.
Other GPIO pins can be used.

![gpio](/_DOCS/assemble/electric/images/gpio.jpg)

## TODO
- LED wiring
