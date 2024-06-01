from fastapi import FastAPI, HTTPException
from api_models import NewVideoRequestParams, TrackedVideoRequestParams
from main_no_track import process_keypoints
from storage import get_input_video, get_keypoints
from save_keypoints import process_video

app = FastAPI()

@app.post("/api/new_video")
async def new_video(params: NewVideoRequestParams):
    video = get_input_video(params.video_name, params.video_extension)
    if not video.is_opened():
        raise HTTPException(status_code = 404, detail = "Video not found")

    process_video(params.video_name, video, params.arm)

    keypoints = get_keypoints(params.video_name)
    if keypoints is None:
        raise HTTPException(status_code = 500, detail = "Couldn't get keypoints")

    calories, calories_abs, calories_from_energy, calories_abs_from_energy = process_keypoints(params.video_name, video, params.distance_elbow_wrist, params.mass_weight, params.mass_forearm, params.radius_bicep, params.height_shoulder, keypoints)
    video.close()

    return {
        "calories": calories,
        "calories_abs": calories_abs,
        "calories_from_energy": calories_from_energy,
        "calories_abs_from_energy": calories_abs_from_energy
    }

@app.post("/api/tracked_video")
async def tracked_video(params: TrackedVideoRequestParams):
    video = get_input_video(params.video_name, params.video_extension)
    if not video.is_opened():
        raise HTTPException(status_code = 404, detail = "Video not found")
    
    keypoints = get_keypoints(params.video_name)
    if keypoints is None:
        raise HTTPException(status_code = 404, detail = "Keypoints not found")

    calories, calories_abs, calories_from_energy, calories_abs_from_energy = process_keypoints(params.video_name, video, params.distance_elbow_wrist, params.mass_weight, params.mass_forearm, params.radius_bicep, params.height_shoulder, keypoints)
    video.close()

    return {
        "calories": calories,
        "calories_abs": calories_abs,
        "calories_from_energy": calories_from_energy,
        "calories_abs_from_energy": calories_abs_from_energy
    }