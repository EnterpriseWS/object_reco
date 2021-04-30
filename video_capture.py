import numpy as np
import cv2
import time


class VideoCapture:
    def __init__(self):
        self._vc = cv2.VideoCapture(0)

    def capture(self, fp=None, is_continuous=False, video_span=0, image_interval=0, max_size=0) -> None:
        while True:
            # Capture frame-by-frame
            ret, frame = self._vc.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            time.sleep(1)

            # Display the resulting frame
            cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self._vc.release()
        cv2.destroyAllWindows()

    def display(self):
        pass
