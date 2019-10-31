import cv2

test_filter_img = cv2.imread("filters/wiet/wiet-glasses.png", -1)
test_filter = (test_filter_img, 0.55)


# skalowanie filtra do szerokosci twarzy
def resize_filter(filter, face, eye_y, offset):  #offset zalezny od filtra
    (x, y, face_width, face_height) = face
    (filter_height, filter_width) = (filter.shape[0], filter.shape[1])
    scale = 1.0 * face_width / filter_width

    filter = cv2.resize(filter, (int(scale * filter_width), int(scale * filter_height)))
    (filter_height, filter_width) = (filter.shape[0], filter.shape[1])
    new_y = eye_y + filter_height - int(filter_height * offset)  # ustalamy nowe polozenie filtru

    if(new_y < 0):  # jezeli filtr wychodzi poza kamere to go ucinamy
        filter = filter[abs(new_y)::, :, :]
        new_y = 0

    return (filter, new_y)


# dodawanie filtra do obrazu
def add_filter(camera, filter, x, eye_y, face):

    (filter_img, offset) = filter
    (filter_img, y) = resize_filter(filter_img, face, eye_y, offset)

    (height, width) = (filter_img.shape[0], filter_img.shape[1])
    (img_height, img_width) = (camera.shape[0], camera.shape[1])

    if x + width >= img_width:  # filtr wychodzi poza obraz z prawej strony
        filter_img = filter_img[:, 0:img_width - x, :]

    if y + height >= img_height:  # filtr wychodzi poza obraz na dole
        filter_img = filter_img[0:img_height - y, :, :]

    if x < 0:  # filtr wychodzi poza ramke z lewej strony
        filter_img = filter_img[:, abs(x)::, :]
        width = filter_img.shape[1]
        x = 0

    filter_alpha = filter_img[:, :, 3]/255.0
    img_alpha = 1 - filter_alpha

    for c in range(3):
        camera[y:y+height, x:x+width, c] = filter_img[:, :, c] * filter_alpha + camera[y:y+height, x:x+width, c] * img_alpha

