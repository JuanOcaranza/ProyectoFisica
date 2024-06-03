import pickle as pkl
import pandas as pd
import cv2 as cv
from .video import Video
import os

# Currently uses file system, should use cloud storage in deploy.

VIDEOS_DIR = "../public/videos"
KEYPOINTS_DIR = "../public/keypoints"
CSV_DIR = "../public/csv"

def get_input_video(name: str, extension: str) -> Video:
    return _get_video(f"{VIDEOS_DIR}/input/{name}.{extension}")

def get_velocity_and_acceleration_video(name: str) -> Video:
    return _get_video(f"{VIDEOS_DIR}/velocity_and_acceleration/{name}.mp4")

def get_forces_video(name: str) -> Video:
    return _get_video(f"{VIDEOS_DIR}/forces/{name}.mp4")

def _get_video(path: str) -> Video:
    return Video(_get_absolute_path(path))

def get_keypoints(name: str) -> list:
    with open(_get_absolute_path(f"{KEYPOINTS_DIR}/{name}"), "rb") as f:
        return pkl.load(f)
    
def save_keypoints(name: str, keypoints: list):
    with open(_get_absolute_path(f"{KEYPOINTS_DIR}/{name}"), "wb") as f:
        pkl.dump(keypoints, f)

def save_data_frame(name: str, df: pd.DataFrame):
    df.to_csv(_get_absolute_path(f"{CSV_DIR}/{name}.csv"), index = False)

def get_data_frame(name: str) -> pd.DataFrame:
    return pd.read_csv(_get_absolute_path(f"{CSV_DIR}/{name}.csv"))

def save_velocity_and_acceleration_video(name: str, frames: list, fps: float, width: int, height: int):
    _save_video(_get_absolute_path(f"{VIDEOS_DIR}/velocity_and_acceleration/{name}.mp4"), frames, fps, width, height)

def save_forces_video(name: str, frames: list, fps: float, width: int, height: int):
    _save_video(_get_absolute_path(f"{VIDEOS_DIR}/forces/{name}.mp4"), frames, fps, width, height)

def _save_video(path: str, frames: list, fps: float, width: int, height: int):
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(path, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()

def _get_absolute_path(path: str) -> str:
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, path)