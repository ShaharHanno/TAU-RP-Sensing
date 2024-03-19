import cv2
from realsense_depth import DepthCamera

point = (400, 300)

def show_distance(event, x, y, args, params):
    global point
    point = (x, y)

# Initialize Camera Intel RealSense
dc = DepthCamera()

# Create mouse event
cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame", show_distance)

while True:
    ret, depth_frame, color_frame = dc.get_frame()

    # Show distance for a specific point
    cv2.circle(color_frame, point, 4, (0, 0, 255))
    
    # Convert depth value from millimeters to meters
    distance_mm = depth_frame[point[1], point[0]]
    distance_m = distance_mm / 1000.0

    cv2.putText(color_frame, "{:.2f}m".format(distance_m), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    #cv2.imshow("Depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
