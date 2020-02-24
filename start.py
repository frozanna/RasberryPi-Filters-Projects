import cv2
from time import sleep
from filters import f_length, add_filters
from detectors import detect_faces
from servo import Servo, get_position
from thread import ServoThread


# inicjalizacja kamery i jej interfejsu
def camera_init():
    print("Initializing camera...")
    for i in range(0, 5):
        camera = cv2.VideoCapture(0
        )
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


def loop(cam_obj, servo):
    i = 0;
    running = True
    while running:
        # pobierz obraz z kamery
        camera = get_image(cam_obj)

        faces = detect_faces(camera)

        for face in faces:
            add_filters(camera, i, face)

        # wyswietl obraz
        cv2.imshow("Smile!", camera)
        
        if len(faces) == 1:
            (camera_height, camera_width) = (camera.shape[0], camera.shape[1])
            (face_x, face_y, face_width, face_height) = faces[0]
            position = get_position(camera_width, face_x, face_width)
            t = ServoThread(position, servo)
            t.start()
        else:
            t = ServoThread(7.5, servo)
            t.start()

        key = cv2.waitKey(1)
        if key == ord('n'):
            i += 1
            i %= f_length
            
        if key == ord('b'):
            i -= 1
            if i < 0:
                i = f_length -1

        # jesli odczytamy wcisniecie klawisza q, to wychodzimy
        if key == ord('q'):
            running = False


def main():
    cam_obj = camera_init()
    servo = Servo()
    loop(cam_obj, servo)
    servo.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
