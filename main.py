from tracker import Tracker
from video import Video
from data import Data
from plotter import Plotter
from adapter import Adapter
from unit_converter import Unit_converter
import column_filter as cf

reference_distance = 0.3
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

objects = ["shoulder", "elbow", "wrist"]
adapter = Adapter(positions, objects, video.get_height())
data = Data(adapter.get_adapted_data(), objects)
df = data.get_data()
unit_converter = Unit_converter(df['r_wrist'].iloc[0], reference_distance, video.get_fps(), 1)
df = unit_converter.convert_position(df, cf.position_columns(df.columns))
df = unit_converter.convert_velocity(df, cf.velocity_columns(df.columns))
df = unit_converter.convert_acceleration(df, cf.acceleration_columns(df.columns))
df = unit_converter.convert_time(df, ['time'])
plotter = Plotter(df)

plotter.show_plot()

video.close()