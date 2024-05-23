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
    
    def _move_yo_dy_origin_to_top_left(self, y0, dy):
        return self.get_height() - y0, -dy
    
    def _move_yo_y1_origin_to_top_left(self, y0, y1):
        return self.get_height() - y0, self.get_height() - y1
    
    def show_with_vectors(self, vectors, lines = [], signs = [], title = "Video"):
        frames_with_vectors = []
        for index, frame in enumerate(self.get_frames()):
            frame_with_vectors = frame.copy()
            for vector in vectors:
                x0s, y0s, dxs, dys, tag, color, scale = vector
                if _is_valid_vector(x0s, y0s, dxs, dys, index):
                    y0_converted, dy_converted = self._move_yo_dy_origin_to_top_left(y0s[index], dys[index])
                    scaled_dx, scaled_dy = dxs[index] * scale, dy_converted * scale
                    _draw_vector(frame_with_vectors, int(x0s[index]), int(y0_converted), int(scaled_dx), int(scaled_dy), tag, color)

            for line in lines:
                x0s, y0s, x1s, y1s = line
                if _is_valid_vector(x0s, y0s, x1s, y1s, index):
                    y0_converted, y1_converted = self._move_yo_y1_origin_to_top_left(y0s[index], y1s[index])
                    _draw_line(frame_with_vectors, int(x0s[index]), int(y0_converted), int(x1s[index]), int(y1_converted))
            
            x_sign = 50
            for sign in signs:
                values, tag, color = sign
                if index < len(values) and not np.isnan(values[index]):
                    _draw_sign(frame_with_vectors, x_sign, values[index] > 0, tag, color)
                    x_sign += 50

            frames_with_vectors.append(frame_with_vectors)
        
        show_and_control(title, frames_with_vectors)

    def close(self):
        self.cap.release()

def _is_valid_vector(x0s, y0s, dxs, dys, index):
    return index < len(x0s) and not np.isnan(x0s[index]) and not np.isnan(y0s[index]) and not np.isnan(dxs[index]) and not np.isnan(dys[index])

def _draw_vector(frame, x0, y0, dx, dy, tag, color):
        x1 = x0 + dx
        y1 = y0 + dy
        cv.arrowedLine(frame, (x0, y0), (x1, y1), color, 2)
        cv.circle(frame, (x0, y0), 3, color, -1)
        cv.putText(frame, tag, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

def _draw_line(frame, x0, y0, x1, y1):
    cv.line(frame, (x0, y0), (x1, y1), (255, 255, 255), 2)
    cv.circle(frame, (x0, y0), 3, (255, 255, 255), -1)
    cv.circle(frame, (x1, y1), 3, (255, 255, 255), -1)

def _draw_sign(frame, x, up, tag, color):
    if up:
        y = 100
        dy = -70
    else:
        y = 30
        dy = 70
    _draw_vector(frame, x, y, 0, dy, tag, color)

def _wait_user():
    wait_frame = np.zeros((100, 400, 3), np.uint8)
    cv.putText(wait_frame, "Press any key to continue", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv.imshow("Wait", wait_frame)
    cv.waitKey(0)
    cv.destroyWindow("Wait")

def show_and_control(title, frames):
        index = -1
        key = -1
        isPaused = False

        while key != ord('q'):
            if key == -1 and not isPaused and index < len(frames) - 1:
                index += 1
            elif key == ord('p'):
                isPaused = not isPaused
            elif key == ord('a') and index > 0:
                index -= 1
                isPaused = True
            elif key == ord('d') and index < len(frames) - 1:
                index += 1
                isPaused = True
            elif key == ord('r'):
                index = 0
                isPaused = True

            cv.imshow(title, frames[index])
            key = cv.waitKey(33)
        
        cv.destroyAllWindows()