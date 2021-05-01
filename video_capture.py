import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
import platform

if platform.system() == 'Linux':
    DEVICE_ID = '/dev/video1'
elif platform.system() == 'Windows':
    DEVICE_ID = 0
FRAME_RATE = 30


class VideoCapture:
    def __init__(self, device=DEVICE_ID, frame_rate=FRAME_RATE):
        # TODO: Setup a config file to keep the constants below instead.
        self._vc = cv2.VideoCapture(device)
        self._vc.set(cv2.CAP_PROP_FPS, frame_rate)
        self._stop_capture = False

    def capture(self, fp=None, is_continuous=False, video_span=0, image_interval=0, max_size=0) -> None:
        ret, frame = self._vc.read()
        current_image = plt.imshow(frame, cmap='gray')
        plt.ion()

        while not self._stop_capture:
            # During the read() action, it blocks the thread.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self._stop_capture = True
                break
            ret, next_frame = self._vc.read()
            cvt_image = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
            current_image.set_data(cvt_image)
            # CAUTION: pause() action is required for displaying correctly,
            #          it yields to the GUI event loop.
            plt.pause(float(1/FRAME_RATE))

        plt.ioff()
        plt.show()
        self._vc.release()
        cv2.destroyAllWindows()
