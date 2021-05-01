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
        try:
            ret, frame = self._vc.read()
            # Reserved for gray images.
            # current_image = plt.imshow(frame, cmap='gray')
            # The initial frame is required for the following frames.
            current_image = plt.imshow(frame)
            plt.ion()

            while not self._stop_capture:
                # # During the read() action, it blocks the thread.
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     self._stop_capture = True
                #     break
                start_time = time.time()
                ret, next_frame = self._vc.read()
                # Reserved for gray images.
                # cvt_image = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
                cvt_image = cv2.cvtColor(next_frame, cv2.COLOR_BGR2RGB)
                current_image.set_data(cvt_image)
                print(f'frame_time: {time.time() - start_time}')
                # CAUTION: pause() action is required for displaying correctly
                #          because it yields to the GUI event loop.
                plt.pause(float(1/FRAME_RATE))

            # NOTE: Both ioff() and show() methods are not needed for displaying
            #       once the set_data() is used.
        except Exception as ex:
            print(f'*** Something wrong: {ex}')
        self._vc.release()
        cv2.destroyAllWindows()
