import time
from rplidar import RPLidar
import serial.serialutil
import os

os.putenv('SDL_FBDEV', '/dev/fb1')

PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

MIN_DISTANCE = 100  # In mm
MAX_DISTANCE = 4000  # In mm

def read_lidar_data(lidar):
    data = []
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            # Filter out invalid or unreliable measurements
            if MIN_DISTANCE < distance < MAX_DISTANCE:  # Adjust the range based on your lidar specifications
                data.append((angle, distance))
        break  # Break after the first complete scan
    return data

def check_distance(data, threshold):
    for (angle, distance) in data:
        if distance < threshold:
            return True, angle, distance  # Object is too close
    return False, None, None

def trigger_alarm(angle, distance):
    print(f"Object detected at angle {angle} degrees with distance {distance} mm. Triggering alarm.")

try:
    counter = 1
    while True:
        lidar_data = read_lidar_data(lidar)
        threshold_distance = 150  # Adjust the threshold as needed
        too_close, detected_angle, detected_distance = check_distance(lidar_data, threshold_distance)
        if too_close:
            trigger_alarm(detected_angle, detected_distance)
            print(counter)
            print("\n--------")
            counter += 1
except KeyboardInterrupt:
    print("Stopping the program.")

finally:
    try:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
    except serial.serialutil.SerialException:
        pass  # Ignore serial port errors during cleanup
