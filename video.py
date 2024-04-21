import cv2 as cv
import numpy as np

class Video:
    def __init__(self, path):
        self.path = path
        self.cap = cv.VideoCapture(path)
        self.frames = []

    def is_opened(self):
        return self.cap.isOpened()

    def get_frames(self):
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
    
    def get_fps(self):
        return self.cap.get(cv.CAP_PROP_FPS)
    
    
    def show_with_vectors(self, vectors):
        for index, frame in enumerate(self.get_frames()):
            for vector in vectors:
                x0s, y0s, dxs, dys, tag, color = vector
                if _is_valid_vector(x0s, y0s, dxs, dys, index):
                    _draw_vector(frame, int(x0s[index]), int(y0s[index]), int(dxs[index]), int(dys[index]), tag, color)

            resized_frame = cv.resize(frame, (640, 480), interpolation=cv.INTER_AREA)
            cv.imshow('Frame', resized_frame)
            if cv.waitKey(33) & 0xFF == ord('q'):
                break
        
        cv.destroyAllWindows()

    def close(self):
        self.cap.release()

def _is_valid_vector(x0s, y0s, dxs, dys, index):
    return index < len(x0s) and not np.isnan(x0s[index]) and not np.isnan(y0s[index]) and not np.isnan(dxs[index]) and not np.isnan(dys[index])

def _draw_vector(frame, x0, y0, dx, dy, tag, color):
    x1 = x0 + dx
    y1 = y0 + dy
    cv.arrowedLine(frame, (x0, y0), (x1, y1), color, 2)
    cv.putText(frame, tag, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)