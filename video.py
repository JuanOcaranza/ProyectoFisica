import cv2 as cv

class Video:
    def __init__(self, path):
        self.path = path
        self.cap = cv.VideoCapture(path)
        self.frames = []

    def is_opened(self):
        return self.cap.isOpened()

    def getFrames(self):
        if self.frames == []:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    self.frames.append(frame)
                else:
                    break
        return self.frames

    def get_height(self):
        return self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)

    def close(self):
        self.cap.release()