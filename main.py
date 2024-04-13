from tracker import Tracker
from video import Video
from data import Data
from plotter import Plotter

tracker = Tracker([6, 8, 10])
video = Video("bicep.mkv")
positions = []

for frame in video.getFrames():
    keypoints = tracker.get_keypoints(frame)

    if len(keypoints) > 0:
        positions.append(keypoints)

video.close()

data = Data(["shoulder", "elbow", "wrist"], positions)
plotter = Plotter(data.get_data())

plotter.show_plot()