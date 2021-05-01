import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import platform

if platform.system() == 'Linux':
    DEVICE_ID = '/dev/video1'
elif platform.system() == 'Windows':
    DEVICE_ID = 0
FRAME_RATE = 30
IMAGE_FILENAME = ''
IMAGE_SAVE_RATE = 2  # By second

vc = cv2.VideoCapture(DEVICE_ID)
vc.set(cv2.CAP_PROP_FPS, FRAME_RATE)
if not vc.isOpened():
    print(f'*** Error: Device {DEVICE_ID} is not active.')
    exit()

ret, frame = vc.read()
current_image = plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cmap='gray')
stop_capture = False


def get_next_frame(i):
    # Get the frame captured by the device (blocked read)
    next_ret, next_frame = vc.read()
    # TODO: Choose the most appropriate color space for detection and training
    current_image.set_data(cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY))


def close(event):
    if event.key == 'q':
        stop_capture = True
        plt.close(event.canvas.figure)


try:
    # Example of creating two subplots
    # --------------------------------
    # subplt1 = plt.subplot(1, 2, 1)
    # subplt2 = plt.subplot(1, 2, 2)

    # Example of save image to a file
    # -------------------------------
    # img_name = "opencv_frame_{}.png".format(img_counter)
    # cv2.imwrite(img_name, frame)

    ani = FuncAnimation(plt.gcf(), get_next_frame, interval=200)
    cid = plt.gcf().canvas.mpl_connect("key_press_event", close)
    plt.show()

except Exception as ex:
    stop_capture = True
    print(f'*** Something wrong: {ex}')

# When everything done, release the capture
vc.release()
cv2.destroyAllWindows()
