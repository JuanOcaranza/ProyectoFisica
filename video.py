import cv2 as cv
import time

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
    
    def show(self, frames):
        '''
            Muestra el video :3 en teoria
        '''
        print('Mostrando video...')
        #fourcc = cv.VideoWriter_fourcc(*'XVID')
        #out = cv.VideoWriter('output.avi', fourcc, self.get_fps(), (self.cap.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH), self.cap.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)))
        if(self.is_opened()):
            fps = self.get_fps()
            print(f"mostrame lo fps pibe {fps}")
            for frame in frames:
                #out.write(frame)
                # time.sleep(1/fps)
                cv.imshow('frame',frame)
                cv.waitKey(25)
            cv.destroyAllWindows()
            # out.release()
        else:
            print('Video cerrado')

    def close(self):
        self.cap.release()