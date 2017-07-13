import cv2


def  camera_open(device_num):
    v_cam = cv2.VideoCapture(device_num)
    v_cam.open(device_num)
    return v_cam

def camera_forever_loop(camera):
    while 1:
        bla, image = camera.read()
        cv2.imshow("image", image)

        blue, green ,red = cv2.split(image)
        get_image_sum(green)
        cv2.waitKey(100)

def get_image_sum(image):
    sum = cv2.sumElems(image)
    print(sum[0])

cam = camera_open(0)
camera_forever_loop(cam)