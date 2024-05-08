from tracker import Tracker
from video import Video
import pickle as pkl

video_name = "video0"
tracker = Tracker([6, 8, 10])
video = Video(f"videos/{video_name}.mkv")
if not video.is_opened():
    print("Video not found")
    exit()

positions = []
for frame in video.get_frames():
    keypoints = tracker.get_keypoints(frame)

    if len(keypoints) > 0:
        positions.append(keypoints)

with open(f"keypoints/{video_name}", "wb") as f:
    pkl.dump(positions, f)