import sys
import os
import cv2 as cv
from picamera2 import Picamera2
import pygame
from gpiozero import AngularServo, PhaseEnableMotor
import json
from time import time
import torch
from torchvision import transforms
import convnets


# SETUP
# Load configs and init servo controller
model_path = os.path.join(sys.path[0], 'models', 'DonkeyNet-15epochs-0.001lr.pth')
to_tensor = transforms.ToTensor()
model = convnets.DonkeyNet()  
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
# Load configs
params_file_path = os.path.join(sys.path[0], 'configs.json')
params_file = open(params_file_path)
params = json.load(params_file)
# Constants
STOP_BUTTON = params['stop_btn']
STEER_CENTER = params['steer_center_angle']
STEER_RANGE = params['steer_range']
STEER_DIR = params['steer_dir']
THROTTLE_LIMIT = params['throttle_limit']
# Init servo 
steer = AngularServo(
    pin=params['steer_pin'], 
    initial_angle=params['steer_center_angle'], 
    min_angle=params['steer_min_angle'], 
    max_angle=params['steer_max_angle'],
)
# Init motor 
throttle = PhaseEnableMotor(
    phase=params['throttle_dir_pin'], 
    enable=params['throttle_pwm_pin'],
)
# Init controller
pygame.display.init()
pygame.joystick.init()
js = pygame.joystick.Joystick(0)
# init camera
cam = Picamera2()
cam.configure(
    cam.create_preview_configuration(
        main={"format": 'RGB888', "size": (120, 160)},
        controls={"FrameDurationLimits": (50000, 50000)},  # 20 FPS
    )
)
cam.start()
for i in reversed(range(60)):
    frame = cam.capture_array()
    # cv.imshow("Camera", frame)
    # cv.waitKey(1)
    if frame is None:
        print("No frame received. TERMINATE!")
        sys.exit()
    if not i % 20:
        print(i/20)  # count down 3, 2, 1 sec  
# Init timer for FPS computing
start_stamp = time()
frame_counts = 0
ave_frame_rate = 0.


# # MAIN
# try:
#     while True:
#         frame = cam.capture_array()  # read image
#         if frame is None:
#             print("No frame received. TERMINATE!")
#             sys.exit()
#         for e in pygame.event.get():  # read controller input
#             if e.type == pygame.JOYBUTTONDOWN:
#                 if js.get_button(STOP_BUTTON):  # emergency stop 
#                     throttle.stop()
#                     throttle.close()
#                     steer.close()
#                     cv.destroyAllWindows()
#                     pygame.quit()
#                     print("E-STOP PRESSED. TERMINATE")
#                     sys.exit()
#         # predict steer and throttle
#         # image = cv.resize(frame, (120, 160))
#         img_tensor = to_tensor(frame)
#         pred_st, pred_th = model(img_tensor[None, :]).squeeze()
#         st_trim = float(pred_st)
#         if st_trim >= 1:  # trim steering signal
#             st_trim = .999
#         elif st_trim <= -1:
#             st_trim = -.999
#         th_trim = (float(pred_th))
#         if th_trim >= 1:  # trim throttle signal
#             th_trim = .999
#         elif th_trim <= -1:
#             th_trim = -.999
#         # Drive servo
#         steer.angle = STEER_CENTER + st_trim * STEER_RANGE * STEER_DIR
#         # Drive motor
#         if th_trim >= 0.1:
#             throttle.forward(min(th_trim, THROTTLE_LIMIT))
#         elif th_trim <= -0.1:
#             throttle.backward(min(-th_trim, THROTTLE_LIMIT))
#         else:
#             throttle.stop()
#         print(f"predicted action: {pred_st, pred_th}")        
#         frame_counts += 1
#         # Log frame rate
#         since_start = time() - start_stamp
#         frame_rate = frame_counts / since_start
#         print(f"frame rate: {frame_rate}")
#         if cv.waitKey(1)==ord('q'):
#             cv.destroyAllWindows()
#             sys.exit()
# except KeyboardInterrupt:
#     cv.destroyAllWindows()
#     sys.exit()
