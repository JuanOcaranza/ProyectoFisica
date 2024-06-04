from pydantic import BaseModel

class NewVideoRequestParams(BaseModel):
    video_name: str
    video_extension: str
    distance_elbow_wrist: float
    mass_weight: float
    mass_forearm: float
    radius_bicep: float
    arm: str

class TrackedVideoRequestParams(BaseModel):
    video_name: str
    video_extension: str
    distance_elbow_wrist: float
    mass_weight: float
    mass_forearm: float
    radius_bicep: float
