import sys
from main_no_track import process_keypoints, show_plot
from storage import get_input_video, get_velocity_and_acceleration_video, get_forces_video
from storage import get_keypoints, get_data_frame
from save_keypoints import process_video

VIDEO_NOT_FOUND = 1
KEYPOINTS_NOT_FOUND = 2

DISTANCE_ELBOW_WRIST =  0.3
MASS_WEIGHT = 1
MASS_FOREARM = 1
RADIUS_BICEP = 0.04
VIDEO_NAME = "video2"
EXTENSION = "mp4"
ARM = "right"

video = get_input_video(VIDEO_NAME, EXTENSION)
if not video.is_opened():
    print("Video not found")
    sys.exit(VIDEO_NOT_FOUND)

process_video(VIDEO_NAME, video, ARM)

keypoints = get_keypoints(VIDEO_NAME)
if keypoints is None:
    print("Keypoints not found")
    sys.exit(KEYPOINTS_NOT_FOUND)

calories, calories_from_energy = process_keypoints(
    VIDEO_NAME, video, DISTANCE_ELBOW_WRIST, MASS_WEIGHT, MASS_FOREARM, RADIUS_BICEP, keypoints)
video.close()

velocity_and_acceleration_video = get_velocity_and_acceleration_video(VIDEO_NAME)
velocity_and_acceleration_video.play("velocity_and_acceleration")
velocity_and_acceleration_video.close()

forces_video = get_forces_video(VIDEO_NAME)
forces_video.play("forces")
forces_video.close()

data_frame = get_data_frame(VIDEO_NAME)
show_plot(data_frame)

print(f"Calories: {calories}")
print(f"Calories from energy: {calories_from_energy}")
