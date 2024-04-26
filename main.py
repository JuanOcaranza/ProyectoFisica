import numpy as np
from tracker import Tracker
from video import Video
from data import Data
from plotter import Plotter
from adapter import Adapter
from unit_converter import Unit_converter
import column_filter as cf
from datetime import datetime

reference_distance = 0.3
mass = 50
tracker = Tracker([6, 8, 10])
video = Video("videos/video3.mp4")
if not video.is_opened():
    print("Video not found")
    exit()

positions = []
objects = ["shoulder", "elbow", "wrist"]

for frame in video.get_frames():
    keypoints = tracker.get_keypoints(frame)

    if len(keypoints) > 0:
        positions.append(keypoints)

adapter = Adapter(positions, objects, video.get_height())
data = Data(adapter.get_adapted_data(), objects)
df = data.get_data()
raw_data = df[:]

unit_converter = Unit_converter(df['r_wrist'].iloc[0], reference_distance, video.get_fps(), 1)
df = unit_converter.convert_position(df, cf.position_columns(df.columns))
df = unit_converter.convert_velocity(df, cf.velocity_columns(df.columns))
df = unit_converter.convert_acceleration(df, cf.acceleration_columns(df.columns))
df = unit_converter.convert_angular_velocity(df, ['angular_velocity'])
df = unit_converter.convert_time(df, ['time'])

plotter = Plotter(df)

raw_data.to_csv(f"csv/raw_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index = False)
df.to_csv(f"csv/data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index = False)

video.show_with_vectors([
    (raw_data['rx_wrist'].values, raw_data['ry_wrist'].values, raw_data['vx_wrist'].values, raw_data['vy_wrist'].values, 'v', (0, 255, 0), video.get_fps()),
    (raw_data['rx_wrist'].values, raw_data['ry_wrist'].values, raw_data['ax_wrist'].values, raw_data['ay_wrist'].values, 'a', (0, 0, 255), video.get_fps() ** 2)
], "Velocity and Acceleration")

plotter.show_plot()

video.close()