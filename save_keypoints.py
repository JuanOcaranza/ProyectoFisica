from tracker import Tracker
from video import Video
from storage import get_input_video, save_keypoints

def process_video(name: str, video: Video, arm: str):
    relevant_keypoints = [6, 8, 10] if arm == "right" else [5, 7, 9]
    tracker = Tracker(relevant_keypoints)

    keypoints_positions = []
    for frame in video.get_frames():
        keypoints = tracker.get_keypoints(frame)
        if len(keypoints) > 0:
            keypoints_positions.append(keypoints)

    save_keypoints(name, keypoints_positions)

if __name__ == "__main__":
    import sys

    VIDEO_NOT_FOUND = 1

    VIDEO_NAME = "video2"
    EXTENSION = "mp4"
    ARM = "left"

    _video = get_input_video(VIDEO_NAME, EXTENSION)
    if not _video.is_opened():
        print("Video not found")
        sys.exit(VIDEO_NOT_FOUND)

    process_video(VIDEO_NAME, _video, ARM)
    _video.close()
