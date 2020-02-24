import cv2

face_detector = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
eyes_detector = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_eye.xml')
nose_detector = cv2.CascadeClassifier('/home/pi/Documents/Projekt/detectors/haarcascade_mcs_nose.xml')
mouth_detector = cv2.CascadeClassifier('/home/pi/Documents/Projekt/detectors/Mouth.xml')


def detect_faces(camera):
    img_grayscale = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(img_grayscale, scaleFactor=1.3, minNeighbors=5)

    return faces


def detect_eyes(camera, face):
    img_grayscale = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)
    (x, y, w, h) = face

    roi_gray = img_grayscale[y:y + h, x:x + w]

    eyes = eyes_detector.detectMultiScale(roi_gray)

    return eyes


def detect_nose(camera, face):
    img_grayscale = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)
    (x, y, w, h) = face

    roi_gray = img_grayscale[y:y + h, x:x + w]

    noses = nose_detector.detectMultiScale(roi_gray)

    return noses


def detect_mouth(camera, face):
    img_grayscale = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)
    (x, y, w, h) = face

    roi_gray = img_grayscale[y:y + h, x:x + w]

    mouth = [(int(w / 3), int(7 * h / 10), int(w / 3), int(h / 7))]
    
    return mouth
