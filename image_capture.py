import numpy as np
import cv2
import matplotlib.pyplot as plt
import platform
import datetime

if platform.system() == 'Linux':
    DEVICE_ID = '/dev/video1'
elif platform.system() == 'Windows':
    DEVICE_ID = 0
FRAME_RATE = 30


class ImageCapture:
    def __init__(self, device=DEVICE_ID, frame_rate=FRAME_RATE):
        # TODO: Setup a config file to keep the constants below instead.
        self._vc = cv2.VideoCapture(device)
        self.camera_ready = False
        self._stop_capture = True
        if self._vc.isOpened():
            # self._vc.set(cv2.CAP_PROP_FPS, frame_rate)
            self.camera_ready = True
            self._stop_capture = False

    def capture(self, display, file_ext='png',       # Display on screen or not (Ture/False)
                directory='images', prefix='image',  # Use pre-defined naming if not specified
                video_span=0, interval=0, max_capture=0) -> None:
        reset = datetime.datetime.now()
        day_of_year = reset.timetuple().tm_yday
        midnight = reset.replace(hour=0, minute=0, second=0, microsecond=0)
        try:
            ret, frame = self._vc.read()
            # Reserved for gray images.
            # current_image = plt.imshow(frame, cmap='gray')
            # The initial frame is required for the following frames.
            current_image = None
            if display:
                current_image = plt.imshow(frame)
                plt.ion()
            save_image = False
            if interval > 0:
                save_image = True  # Always take the first image

            while not self._stop_capture:
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     self._stop_capture = True
                #     break
                now = datetime.datetime.now()
                seconds_elapsed = (now - reset).total_seconds()
                if 0 < interval <= seconds_elapsed:
                    save_image = True
                    reset = now
                # During the read() action, it blocks the thread.
                ret, next_frame = self._vc.read()
                # Reserved for gray images.
                # cvt_image = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
                cvt_image = cv2.cvtColor(next_frame, cv2.COLOR_BGR2RGB)
                if display:
                    current_image.set_data(cvt_image)
                if save_image:
                    # Create file name as <prefix>_<day_of_year>_<second_of_day>.<file_ext>
                    new_day_of_year = reset.timetuple().tm_yday
                    if new_day_of_year > day_of_year:
                        day_of_year = new_day_of_year
                        midnight = reset.replace(hour=0, minute=0, second=0, microsecond=0)
                    second_of_day = int((reset - midnight).total_seconds())
                    filename = f'{directory}/{prefix}_{day_of_year}_{second_of_day}.{file_ext}'.lower()
                    cv2.imwrite(filename, next_frame)
                # CAUTION: pause() action is required for displaying correctly
                #          because it yields to the GUI event loop.
                if display:
                    plt.pause(float(1/FRAME_RATE))

            # NOTE: Both ioff() and show() methods are not needed for displaying
            #       once the set_data() is used.
        except Exception as ex:
            print(f'*** Something wrong: {ex}')
        self._vc.release()
        cv2.destroyAllWindows()
