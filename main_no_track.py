import pandas as pd
from video import Video
from data import Data
from plotter import Plotter
from adapter import Adapter
from unit_converter import Unit_converter
import column_filter as cf
from forces import Forces
from energy import Energy
from storage import get_input_video, get_velocity_and_acceleration_video, get_forces_video
from storage import get_keypoints, save_velocity_and_acceleration_video, save_forces_video
from storage import save_data_frame, get_data_frame
from fitter import Fitter

JOULES_PER_CALORIE = 4.184

def process_keypoints(name: str, video: Video, distance_elbow_wrist: float,
                      mass_weight: float, mass_forearm: float, radius_bicep: float,
                      keypoints: list) -> tuple[float, float]:
    objects = ["shoulder", "elbow", "wrist"]
    adapter = Adapter(keypoints, objects, video.get_height())
    data = Data(adapter.get_adapted_data(), objects)
    df = data.get_data()
    raw_data = df[:]

    unit_converter = Unit_converter(df['r_wrist'].iloc[0], distance_elbow_wrist, video.get_fps(), 1)
    df = unit_converter.convert_position(df, cf.position_columns(df.columns))
    df = unit_converter.convert_velocity(df, cf.velocity_columns(df.columns))
    df = unit_converter.convert_acceleration(df, cf.acceleration_columns(df.columns))
    df = unit_converter.convert_angular_velocity(df, ['angular_velocity'])
    df = unit_converter.convert_angular_acceleration(df, ['angular_acceleration'])
    df = unit_converter.convert_time(df, ['time'])
    df = unit_converter.convert_position(df, [
        'distance_elbow_shoulder', 'x_vector_elbow_to_shoulder', 'y_vector_elbow_to_shoulder'])

    forces = Forces(df, mass_forearm, mass_weight, radius_bicep)
    df = forces.get_data_with_forces()
    work = forces.get_work()
    calories = work / JOULES_PER_CALORIE

    energy = Energy(df, mass_weight, mass_forearm)
    work_from_energy = energy.get_work()
    calories_from_energy = work_from_energy / JOULES_PER_CALORIE

    fitter = Fitter(df)
    df = fitter.get_df()

    save_data_frame(name, df)

    df = unit_converter.revert_position(df, ['rx_bicep', 'ry_bicep'])

    velocity_and_acceleration_frames = video.copy_with_vectors([
        (raw_data['rx_wrist'].values, raw_data['ry_wrist'].values, raw_data['vx_wrist'].values,
            raw_data['vy_wrist'].values, 'v', (0, 255, 0), video.get_fps()),
        (raw_data['rx_wrist'].values, raw_data['ry_wrist'].values, raw_data['ax_wrist'].values,
            raw_data['ay_wrist'].values, 'a', (0, 0, 255), video.get_fps() ** 2)
    ])
    save_velocity_and_acceleration_video(
        name, velocity_and_acceleration_frames, video.get_fps(),
        video.get_width(), video.get_height()
    )

    forces_frames = video.copy_with_vectors([
        (df['rx_bicep'].values, df['ry_bicep'].values, df['fx_bicep'].values,
            df['fy_bicep'].values, 'f_bicep', (0, 255, 0), 1),
        (raw_data['rx_forearm'].values, raw_data['ry_forearm'].values, df['px_forearm'].values,
            df['py_forearm'].values, 'p_forearm', (0, 0, 255), 5),
        (raw_data['rx_wrist'].values, raw_data['ry_wrist'].values, df['px_weight'].values,
            df['py_weight'].values, 'p_weight', (255, 0, 0), 5)
    ], [
        (raw_data['rx_shoulder'].values, raw_data['ry_shoulder'].values,
            raw_data['rx_elbow'].values, raw_data['ry_elbow'].values),
        (raw_data['rx_elbow'].values, raw_data['ry_elbow'].values,
            raw_data['rx_wrist'].values, raw_data['ry_wrist'].values)
    ], [
        (df['angular_velocity'].values, 'v', (255, 0, 255)),
        (df['angular_acceleration'].values, 'a', (0, 255, 255)),
        (df['sum_moment'].values, 'M', (255, 255, 0))
    ])
    save_forces_video(name, forces_frames, video.get_fps(), video.get_width(), video.get_height())

    return calories, calories_from_energy

def show_plot(df: pd.DataFrame):
    plotter = Plotter(df)
    plotter.show_plot()

if __name__ == "__main__":
    import sys

    VIDEO_NOT_FOUND = 1
    KEYPOINTS_NOT_FOUND = 2

    DISTANCE_ELBOW_WRIST =  0.3
    MASS_WEIGHT = 1
    MASS_FOREARM = 1
    RADIUS_BICEP = 0.04
    VIDEO_NAME = "video2"
    EXTENSION = "mp4"

    _video = get_input_video(VIDEO_NAME, EXTENSION)
    if not _video.is_opened():
        print("Video not found")
        sys.exit(VIDEO_NOT_FOUND)

    _keypoints = get_keypoints(VIDEO_NAME)
    if _keypoints is None:
        print("Keypoints not found")
        sys.exit(KEYPOINTS_NOT_FOUND)

    _calories, _calories_from_energy = process_keypoints(
        VIDEO_NAME, _video, DISTANCE_ELBOW_WRIST, MASS_WEIGHT, MASS_FOREARM,
        RADIUS_BICEP, _keypoints
    )
    _video.close()

    velocity_and_acceleration_video = get_velocity_and_acceleration_video(VIDEO_NAME)
    velocity_and_acceleration_video.play("velocity_and_acceleration")
    velocity_and_acceleration_video.close()

    forces_video = get_forces_video(VIDEO_NAME)
    forces_video.play("forces")
    forces_video.close()

    data_frame = get_data_frame(VIDEO_NAME)
    show_plot(data_frame)

    print(f"Calories: {_calories}")
    print(f"Calories from energy: {_calories_from_energy}")
