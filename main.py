from tracker import Tracker
from video import Video
from data import Data
from plotter import Plotter
from adapter import Adapter
from unit_converter import Unit_converter
import column_filter as cf
from datetime import datetime
from forces import Forces
import re

reference_distance = 0.3
mass = 50
tracker = Tracker([6, 8, 10])
video = Video("videos/video0.mkv")
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

unit_converter = Unit_converter(df['r_wrist'].iloc[0], reference_distance, video.get_fps(), 1)
df = unit_converter.convert_position(df, cf.position_columns(df.columns))
df = unit_converter.convert_velocity(df, cf.velocity_columns(df.columns))
df = unit_converter.convert_acceleration(df, cf.acceleration_columns(df.columns))
df = unit_converter.convert_angular_velocity(df, ['angular_velocity'])
df = unit_converter.convert_time(df, ['time'])

plotter = Plotter(df)

df = Forces(df, mass).get_data_with_forces()

df.to_csv(f"csv/data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index = False)

reversed_unit_converter = unit_converter.get_reversed_unit_converter()
df = reversed_unit_converter.convert_position(df, cf.position_columns(df.columns))
df = reversed_unit_converter.convert_force(df, cf.force_columns(df.columns))
for column in [column for column in df.columns if re.match("ry_", column)]:
    df[column] = video.get_height() - df[column]
for column in [column for column in df.columns if re.match("fy_", column)]:
    df[column] = -1 * df[column]

vectors = [
    (df['rx_wrist'].values, df['ry_wrist'].values, df['fx_g'].values, df['fy_g'].values, 'g', (0, 255, 0)),
    (df['rx_wrist'].values, df['ry_wrist'].values, df['fx_not_g'].values, df['fy_not_g'].values, 'not_g', (255, 0, 0)),
    (df['rx_wrist'].values, df['ry_wrist'].values, df['fx_total'].values, df['fy_total'].values, 'total', (0, 0, 255))
]

video.show_with_vectors(vectors)
plotter.show_plot()

video.close()