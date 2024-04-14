from tracker import Tracker
from video import Video
from data import Data
from plotter import Plotter
from adapter import Adapter

tracker = Tracker([6, 8, 10])
video = Video("videos/video0.mkv")
if not video.is_opened():
    print("Video not found")
    exit()

positions = []

for frame in video.getFrames():
    keypoints = tracker.get_keypoints(frame)

    if len(keypoints) > 0:
        positions.append(keypoints)

video.close()

objects = ["shoulder", "elbow", "wrist"]
adapter = Adapter(positions, objects, video.get_height())
data = Data(adapter.get_adapted_data(), objects)
plotter = Plotter(data.get_data())

plotter.show_plot()