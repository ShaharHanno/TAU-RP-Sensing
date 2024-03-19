import time
import pyrealsense2 as rs

# Initialize the RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: depth
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        if depth_frame:
            # Get the depth value at the center of the frame
            width, height = depth_frame.get_width(), depth_frame.get_height()
            center_x, center_y = width // 2, height // 2
            depth_value = depth_frame.get_distance(center_x, center_y)
            
            # Print the depth value to the terminal
            print(f"Depth at center point: {depth_value:.2f} meters")

        # Wait for 1 second before the next iteration
        time.sleep(1)

finally:
    # Stop streaming
    pipeline.stop()
