import pygame
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()


def get_snapshot():
    cam = pygame.camera.Camera("/dev/video0", (640, 480))
    cam.start()
    image = cam.get_image()


def get_cam_list():
    camlist = pygame.camera.list_cameras()
    if camlist:
        cam = pygame.camera.Camera(camlist[0], (640, 480))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_snapshot()
