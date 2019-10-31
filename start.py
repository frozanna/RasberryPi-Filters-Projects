import cv2
import sys
import os
from time import sleep
from filters import test_filter, add_filter
from detectors import detect_faces, detect_eyes


# inicjalizacja kamery i jej interfejsu
def camera_init():
    print("Initializing camera...")
    for i in range(0, 5):
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if camera.isOpened():
            print("Camera init OK")
            return camera
        sleep(1)
    print("Camera init failed")
    exit()


# funkcja upraszczajaca odczyt z kamery
def get_image(camera):
    (ret, frame) = camera.read()
    return frame


def loop(running, cam_obj):

    while(running):
        # pobierz obraz z kamery
        img = get_image(cam_obj)

        faces = detect_faces(img)

        for face in faces:
            eyes = detect_eyes(img, face)
            if len(eyes) == 2:
                (x1, y1, w1, h1) = eyes[0]
                (x2, y2, w2, h2) = eyes[1]
                add_filter(img, test_filter, int(x1 + x2 + w2 + w1), y1, face)

        # wyswietl obraz
        cv2.imshow("Smile!", img)

        # jesli odczytamy wcisniecie klawisza q, to wychodzimy
        if cv2.waitKey(1) == ord('q'):
            running = False

    sleep(1)


def main():
    cam_obj = camera_init()
    running = True
    loop(running, cam_obj)


if __name__ == "__main__":
    main()
