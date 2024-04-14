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
        # I don't undersand why, but cv.CAP_PROP_FRAME_HEIGHT is not working (always returns 0)
        return self.getFrames()[0].shape[0]

    def close(self):
        self.cap.release()