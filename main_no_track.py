import numpy as np
from video import Video
from data import Data
from plotter import Plotter
from adapter import Adapter
from unit_converter import Unit_converter
import column_filter as cf
from forces import Forces
import pickle as pkl
from energy import Energy

joules_per_calorie = 4.184
reference_distance = 0.3
mass_weight = 1
mass_forearm = 1
radius_bicep = 0.04
height_shoulder = 1.05
video_name = "video2"
video = Video(f"videos/{video_name}.mp4")
if not video.is_opened():
    print("Video not found")
    exit()

objects = ["shoulder", "elbow", "wrist"]

with open(f"keypoints/{video_name}", "rb") as f:
    positions = pkl.load(f)

adapter = Adapter(positions, objects, video.get_height())
data = Data(adapter.get_adapted_data(), objects)
df = data.get_data()
raw_data = df[:]

unit_converter = Unit_converter(df['r_wrist'].iloc[0], reference_distance, video.get_fps(), 1)
df = unit_converter.convert_position(df, cf.position_columns(df.columns))
df = unit_converter.convert_velocity(df, cf.velocity_columns(df.columns))
df = unit_converter.convert_acceleration(df, cf.acceleration_columns(df.columns))
df = unit_converter.convert_angular_velocity(df, ['angular_velocity'])
df = unit_converter.convert_angular_acceleration(df, ['angular_acceleration'])
df = unit_converter.convert_time(df, ['time'])
df = unit_converter.convert_position(df, ['distance_elbow_shoulder', 'x_vector_elbow_to_shoulder', 'y_vector_elbow_to_shoulder'])

forces = Forces(df, mass_forearm, mass_weight, radius_bicep)
df = forces.get_data_with_forces()
work, work_abs = forces.get_work()
calories = work / joules_per_calorie
calories_abs = work_abs / joules_per_calorie

energy = Energy(df, mass_weight, height_shoulder)
work_from_energy, work_abs_from_energy = energy.get_work()
calories_from_energy = work_from_energy / joules_per_calorie
calories_abs_from_energy = work_abs_from_energy / joules_per_calorie

plotter = Plotter(df)

df = unit_converter.revert_position(df, ['rx_bicep', 'ry_bicep'])

video.show_with_vectors([
    (raw_data['rx_wrist'].values, raw_data['ry_wrist'].values, raw_data['vx_wrist'].values, raw_data['vy_wrist'].values, 'v', (0, 255, 0), video.get_fps()),
    (raw_data['rx_wrist'].values, raw_data['ry_wrist'].values, raw_data['ax_wrist'].values, raw_data['ay_wrist'].values, 'a', (0, 0, 255), video.get_fps() ** 2)
], title = "Velocity and Acceleration")

video.show_with_vectors([
        (df['rx_bicep'].values, df['ry_bicep'].values, df['fx_bicep'].values, df['fy_bicep'].values, 'f_bicep', (0, 255, 0), 1),
        (raw_data['rx_forearm'].values, raw_data['ry_forearm'].values, df['px_forearm'].values, df['py_forearm'].values, 'p_forearm', (0, 0, 255), 5),
        (raw_data['rx_wrist'].values, raw_data['ry_wrist'].values, df['px_weight'].values, df['py_weight'].values, 'p_weight', (255, 0, 0), 5)
    ], [
        (raw_data['rx_shoulder'].values, raw_data['ry_shoulder'].values, raw_data['rx_elbow'].values, raw_data['ry_elbow'].values),
        (raw_data['rx_elbow'].values, raw_data['ry_elbow'].values, raw_data['rx_wrist'].values, raw_data['ry_wrist'].values)
    ], [
        (df['angular_velocity'].values, 'v', (255, 0, 255)),
        (df['angular_acceleration'].values, 'a', (0, 255, 255)),
        (df['sum_moment'].values, 'M', (255, 255, 0))
    ],
    "Forces")

plotter.show_plot()

video.close()

print(f"Calories: {calories}")
print(f"Calories abs: {calories_abs}")
print(f"Calories from energy: {calories_from_energy}")
print(f"Calories abs from energy: {calories_abs_from_energy}")