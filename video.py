import cv2 as cv

class Video:
    def __init__(self, path):
        self.path = path
        self.cap = cv.VideoCapture(path)

    def getFrames(self):
        frames = []
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frames.append(frame)
            else:
                break
        return frames

    def close(self):
        self.cap.release()