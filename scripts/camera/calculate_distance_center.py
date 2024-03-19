import cv2
import numpy as np
import pyrealsense2 as rs

def capture_color_image_with_distance(save_path):
    
    # Configure color and depth streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    # Start streaming
    profil = pipeline.start(config)
    for i in range(5):
        pipeline.wait_for_frames()
    sensor = pipeline.get_active_profile().get_device().query_sensors()[1]
    sensor.set_option(rs.option.exposure, 230.000)


    try:
        # Wait for a coherent set of frames
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            print("No color or depth frame received")
            return

        # Convert the color frame to a numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Apply gamma correction to the color image
        gamma = 0.7  # You can adjust this value
        color_image_corrected = np.power(color_image / 255.0, gamma) * 255.0
        color_image_corrected = color_image_corrected.astype(np.uint8)

        # Apply histogram equalization separately on each channel
        equalized_channels = [cv2.equalizeHist(channel) for channel in cv2.split(color_image_corrected)]
        color_image_equalized = cv2.merge(equalized_channels)

        # Get image dimensions
        height, width, _ = color_image_equalized.shape

        # Calculate the distance to the center of the image
        center_x, center_y = width // 2, height // 2
        distance_to_center = depth_frame.get_distance(center_x, center_y)

        # Overlay the distance on the image
        cv2.putText(color_image_equalized, f"Distance: {distance_to_center:.2f} meters", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Save the color image with the distance information
        cv2.imwrite(save_path, color_image_equalized)
        print(f"Color image with distance saved at: {save_path}")

    finally:
        # Stop streaming
        pipeline.stop()

# Specify the path to save the color image with distance
save_path = "/home/pi/color_image_with_distance.jpeg"

# Capture and save the color image with distance
capture_color_image_with_distance(save_path)
