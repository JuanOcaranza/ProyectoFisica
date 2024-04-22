from tracker import Tracker
from video import Video
from data import Data
from plotter import Plotter
from adapter import Adapter
from unit_converter import Unit_converter
import column_filter as cf
from datetime import datetime
import cv2 as cv
import numpy as np

reference_distance = 0.3
tracker = Tracker([6, 8, 10])
video = Video("videos/video0.mkv")
if not video.is_opened():
    print("Video not found")
    exit()

positions = []

for frame in video.get_frames():
    keypoints = tracker.get_keypoints(frame)

    if len(keypoints) > 0:
        positions.append(keypoints)

objects = ["shoulder", "elbow", "wrist"]
adapter = Adapter(positions, objects, video.get_height())
data = Data(adapter.get_adapted_data(), objects)
df = data.get_data()
raw_data = df[:]

unit_converter = Unit_converter(df['r_wrist'].iloc[0], reference_distance, video.get_fps(), 1, 1, 1)
df = unit_converter.convert_position(df, cf.position_columns(df.columns))
df = unit_converter.convert_velocity(df, cf.velocity_columns(df.columns))
df = unit_converter.convert_acceleration(df, cf.acceleration_columns(df.columns))
df = unit_converter.convert_angular_velocity(df, ['angular_velocity'])
df = unit_converter.convert_time(df, ['time'])


raw_data.to_csv(f"csv/raw_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index = False)
df.to_csv(f"csv/data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index = False)
plotter = Plotter(df)

#plotter.show_plot()
vx_sig = 0
vy_sig = 0
delta_t = 1 / video.get_fps()
frames = video.get_frames()
height = video.get_height()
for i, frame in enumerate(frames):
    if(i > 360):
        break
    #rx_wrist = round(raw_data.at[i - 1, 'rx_wrist'])
    #ry_wrist = int(height - round(raw_data.at[i - 1, 'ry_wrist']))
    rx_wrist = round(raw_data.at[i, 'rx_wrist'])
    ry_wrist = int(height - round(raw_data.at[i, 'ry_wrist']))
    
    vx_wrist = raw_data.at[i, 'vx_wrist'] if not np.isnan(raw_data.at[i, 'vx_wrist']) else 0
    vy_wrist = raw_data.at[i, 'vy_wrist'] if not np.isnan(raw_data.at[i, 'vy_wrist']) else 0


    # vx_sig = raw_data.at[i+1, 'vx_wrist'] if not np.isnan(raw_data.at[i, 'vx_wrist']) else 0
    # vy_sig = raw_data.at[i+1, 'vy_wrist'] if not np.isnan(raw_data.at[i, 'vy_wrist']) else 0


    print(f"{i} Los valores redondeados son {rx_wrist} {ry_wrist} {vx_wrist} {vy_wrist}")
    print(f"Los siguientes son {vx_sig} y {vy_sig}")
    cv.circle(frame, (rx_wrist, ry_wrist), 5, (0,0,255), -1)
    if(i<360):
        print(f"Entra en la iteracion {i}")
        cv.line(frame, (rx_wrist, ry_wrist), (round(rx_wrist + (vx_wrist)), round(ry_wrist + (vy_wrist))), (0, 0, 255), 5)
    else:
        print(f"No entra en la iteracion {i}")

    rx_shoulder = round(raw_data.at[i, 'rx_shoulder'])
    ry_shoulder = int(height - round(raw_data.at[i, 'ry_shoulder']))
    print(f"{i} Los valores redondeados son {rx_shoulder} {ry_shoulder}")
    cv.circle(frame, (rx_shoulder, ry_shoulder), 10, (255,0,0), -1)

    rx_elbow = round(raw_data.at[i, 'rx_elbow'])
    ry_elbow = int(height - round(raw_data.at[i, 'ry_elbow']))
    print(f"{i} Los valores redondeados son {rx_elbow} {ry_elbow}")
    cv.circle(frame, (rx_elbow, ry_elbow), 10, (0,255,0), -1)
video.show(frames)

video.close()