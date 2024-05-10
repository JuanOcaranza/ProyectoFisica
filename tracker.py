from ultralytics import YOLO
import numpy as np
import cv2 as cv
from video import Video
import torch

"""
Single object tracker, able to detect people keypoints and track them.
"""
class Tracker:
    def __init__(self, keypoints_indexes: list[int], model_path = "yolov8n-pose.pt"):
        """
        Initialize the model with the given model path. If model doesn't exist, it will be downloaded.

        Keypoints_indexes is a list of the indexes of the keypoints to track.
            Possible indexes:
                0: nose
                1: left_eye
                2: right_eye
                3: left_ear
                4: right_ear
                5: left_shoulder
                6: right_shoulder
                7: left_elbow
                8: right_elbow
                9: left_wrist
                10: right_wrist
                11: left_hip
                12: right_hip
                13: left_knee
                14: right_knee
                15: left_ankle
                16: right_ankle
        """
        self.keypoints_indexes = keypoints_indexes
        self.model = YOLO(model_path)
        if torch.cuda.is_available():
            self.model.to('cuda')

    def _track(self, frame):
        """
        Track a frame using the model and return the tracked object.
        Parameters:
            frame: the frame to track.
        Returns:
            the tracked object.
        """
        return self.model.track(frame, persist=True)[0]
    
    def _get_keypoints_from_result(self, result):
        """
        Get keypoints from the given result and return a subset based on pre-defined indices.
        """
        keypoints = np.array(result.keypoints.xy.cpu(), dtype = np.int32)[0]
        
        if keypoints.size == 0:
            return []
        
        return [keypoints[keypoint_index] for keypoint_index in self.keypoints_indexes]
    
    def get_keypoints(self, frame):
        """
        Get keypoints position from a given frame.

        Parameters:
            frame (numpy.ndarray): The frame from which keypoints are to be extracted.

        Returns:
            list: A list of keypoints positions.
        """
        return self._get_keypoints_from_result(self._track(frame))
    
if __name__ == "__main__":
    tracker = Tracker([6, 8, 10])
    video = Video("videos/video3.mp4")

    for frame in video.get_frames():
        result = tracker._track(frame)
        keypoints = tracker._get_keypoints_from_result(result)
        annotated_frame = result.plot()

        for index, value in enumerate(keypoints):
            x, y = value[0], value[1]
            cv.putText(annotated_frame, str(index), (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv.imshow("Frame", annotated_frame)
        print(keypoints)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    video.close()
    cv.destroyAllWindows()