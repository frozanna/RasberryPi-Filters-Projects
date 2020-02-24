import cv2
from detectors import detect_eyes, detect_nose, detect_mouth

#(oczy,nos,usta,twarz)
filters = [(("filters/wiet/wiet-glasses.png", 0.55, 1),None,None,None),
             (None,("filters/dog/dog_nose.png", 0.2, 0.4),
             ("filters/dog/dog_tongue.png", -0.1, 0.4),
             ("filters/dog/dog_ears.png", 0.6, 1.2)),
            (None,None,None,("filters/flowers/flowers.png", 0.8, 1.1)),
            (None,None,None,("filters/cathat/cat_hat.png", 0.5, 1.6)),
            (None,None,None,("filters/crown/crown.png", 0.7, 1.1)),
            (None,None,None,("filters/hearts/hearts.png", 0.8, 1.3)),
            (None,("filters/cat/cat_nose.png", 0.15, 0.4),None,
             ("filters/cat/cat_ears.png", 0.6, 1.2)),
            (None,("filters/moustache/moustache.png", -1, 0.6),None,None),
            (None,None,None,("filters/anon/anonymous.png", 0, 0.85))
          ]

f_length = len(filters)


# skalowanie filtra do szerokosci twarzy
def resize_filter(filter, face, elem_y, offset, start_scale):  # offset zalezny od filtra

    (x, y, face_width, face_height) = face
    (filter_height, filter_width) = (filter.shape[0], filter.shape[1])
    scale = start_scale * 1.0 * face_width / filter_width
    
    filter = cv2.resize(filter, (int(scale * filter_width), int(scale * filter_height)))
    (filter_height, filter_width) = (filter.shape[0], filter.shape[1])
    new_y = y + elem_y - int(filter_height * offset) # ustalamy nowe polozenie filtru
    
    return (filter, new_y)


def add_filters(camera, index, face):
    (eyes_f, nose_f, mouth_f, face_f) = filters[index]
    (x, y, w, h) = face
    
    if eyes_f:
        eyes = detect_eyes(camera, face)
        if len(eyes) == 2:
            (eye_x, eye_y, eye_w, eye_h) = eyes[0]
            add_filter(camera, eyes_f, x, eye_y, face, False)
    
    if nose_f:
        noses = detect_nose(camera, face)
        if len(noses) > 0:
            (nose_x, nose_y, nose_w, nose_h) = noses[0]
            add_filter(camera, nose_f, x + nose_x + int(nose_w / 2), nose_y, face, True)

    if mouth_f:
        mouths = detect_mouth(camera, face)
        if len(mouths) > 0:
            (mouth_x, mouth_y, mouth_w, mouth_h) = mouths[0]
            add_filter(camera, mouth_f, x + mouth_x + int(mouth_w / 2), mouth_y, face, True)
            
    if face_f:
        add_face_filter(camera, face_f, face)
        
    
# dodawanie filtra do obrazu
def add_filter(camera, filter, x, start_y, face, x_offset):
    (filter_path, offset, scale) = filter
    filter_start_img = cv2.imread(filter_path, -1)
    (filter_img, y) = resize_filter(filter_start_img, face, start_y, offset, scale)
    (filter_height, filter_width) = (filter_img.shape[0], filter_img.shape[1])
    if x_offset:
        x = x - int(filter_width / 2)

    merge_imgs(camera, filter_img, x, y)
    
        
def add_face_filter(camera, filter, face):
    (face_x, face_y, face_w, face_h) = face
    (filter_path, offset, scale) = filter
    filter_start_img = cv2.imread(filter_path, -1)
    (filter_img, y) = resize_filter(filter_start_img, face, 0, offset, scale)
    x = int(face_x - (face_w * scale - face_w) / 2)
    
    merge_imgs(camera, filter_img, x, y)
    
    
def merge_imgs(camera, filter_img, x, y):
    (height, width) = (filter_img.shape[0], filter_img.shape[1])
    (camera_height, camera_width) = (camera.shape[0], camera.shape[1])

    if y < 0:  # jezeli filtr wychodzi poza kamere to go ucinamy
        filter_img = filter_img[abs(y)::, :, :]
        height = filter_img.shape[0]
        y = 0

    if x + width >= camera_width:  # filtr wychodzi poza obraz z prawej strony
        filter_img = filter_img[:, 0:camera_width - x, :]

    if y + height >= camera_height:  # filtr wychodzi poza obraz na dole
        filter_img = filter_img[0:camera_height - y, :, :]

    if x < 0:  # filtr wychodzi poza ramke z lewej strony
        filter_img = filter_img[:, abs(x)::, :]
        width = filter_img.shape[1]
        x = 0

    filter_alpha = filter_img[:, :, 3]/255.0
    camera_alpha = 1 - filter_alpha

    for c in range(3):
        camera[y:y+height, x:x+width, c] = filter_img[:, :, c] * filter_alpha + camera[y:y+height, x:x+width, c] * camera_alpha
    