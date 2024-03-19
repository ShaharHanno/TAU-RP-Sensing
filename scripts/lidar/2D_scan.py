import os
from math import cos, sin, pi, floor
import pygame
from rplidar import RPLidar
import serial.serialutil


SCALING_FACTOR = 3 # Change this to increase or decrease the window size


# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((320*SCALING_FACTOR, 240*SCALING_FACTOR))
pygame.mouse.set_visible(False)
lcd.fill((0, 0, 0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

# used to scale data to fit on the screen
max_distance = 0

# pylint: disable=redefined-outer-name,global-statement

def process_data(data):
    global max_distance
    lcd.fill((0, 0, 0))
    for angle in range(360):
        distance = data[angle]
        if distance > 0:  # ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            px = 160 + int(x / max_distance * 119)
            py = 120 + int(y / max_distance * 119)
            point = (px*SCALING_FACTOR,py*SCALING_FACTOR)
            lcd.set_at(point, pygame.Color(255, 255, 255))
    pygame.display.update()

scan_data = [0] * 360

try:
    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

        # Handle events, check for Escape key
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise KeyboardInterrupt  # Manually raise KeyboardInterrupt to break out of the loop

except KeyboardInterrupt:
    print('Stopping.')
finally:
    try:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
    except serial.serialutil.SerialException:
        pass  # Ignore serial port errors during cleanup

    pygame.quit()
