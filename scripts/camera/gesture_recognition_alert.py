import cv2
import numpy as np
import pyrealsense2 as rs

# Initialize the RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

# Create a colorizer for the depth stream
colorizer = rs.colorizer()

# Set the desired distance for object detection (in meters)
target_distance = 0.75

# Font settings for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
font_color = (0, 255, 0)  # Green color

# Main loop
try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # Convert depth frame to numpy array
        depth_image = np.asanyarray(colorizer.colorize(depth_frame).get_data())

        # Convert color frame to numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Extract the depth value at the center of the image
        center_x, center_y = color_image.shape[1] // 2, color_image.shape[0] // 2
        depth_value = depth_frame.get_distance(center_x, center_y)

        # Check if the object is within the desired distance
        if depth_value > 0 and depth_value < target_distance:
            # Display "Proximity Alert" and distance in the middle of the screen
            alert_text = "Proximity Alert"
            distance_text = f"Distance: {depth_value:.2f} meters"
            text_size_alert = cv2.getTextSize(alert_text, font, font_scale, font_thickness)[0]
            text_size_distance = cv2.getTextSize(distance_text, font, font_scale, font_thickness)[0]

            # Calculate the position to center the text
            alert_position = ((color_image.shape[1] - text_size_alert[0]) // 2, color_image.shape[0] // 2 - 50)
            distance_position = ((color_image.shape[1] - text_size_distance[0]) // 2, color_image.shape[0] // 2 + 50)

            # Draw the text on the image
            cv2.putText(color_image, alert_text, alert_position, font, font_scale, font_color, font_thickness)
            cv2.putText(color_image, distance_text, distance_position, font, font_scale, font_color, font_thickness)

        # Display the frames
        cv2.imshow("Color Image", color_image)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
