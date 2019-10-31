import cv2

# face_detector = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
# face_detector = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_eye.xml')

face_detector = cv2.CascadeClassifier('C:\\Users\\Ania\\PycharmProjects\\RasberryPI\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
eyes_detector = cv2.CascadeClassifier('C:\\Users\\Ania\\PycharmProjects\\RasberryPI\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_eye.xml')


def detect_faces(camera):
    img_grayscale = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(img_grayscale, scaleFactor=1.3, minNeighbors=5)

    # print("faces detected: ", len(faces))

    return faces


def detect_eyes(camera, face):
    img_grayscale = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)
    (x, y, w, h) = face

    roi_gray = img_grayscale[y:y + h, x:x + w]

    eyes = eyes_detector.detectMultiScale(roi_gray)
    roi_color = camera[y:y + h, x:x + w]
    for (eye_x, eye_y, eye_w, eye_h) in eyes:
        cv2.rectangle(roi_color, (eye_x, eye_y), (eye_x + eye_w, eye_y + eye_h), (0, 255, 0), 2)

    # print("eyes detected: ", len(eyes))

    return eyes