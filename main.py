import image_capture

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    vc = image_capture.ImageCapture()
    if vc.camera_ready:
        vc.capture(True, interval=3)
