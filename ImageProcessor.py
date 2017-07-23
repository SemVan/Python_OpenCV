import cv2
import asyncio
import numpy as np

class ImageProcessor:

    def __init__(self, period):
        self.face = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        self.result_array = []
        self.discrete_period = period
        return

    def  camera_open(self, device_num):
        v_cam = cv2.VideoCapture(device_num)
        v_cam.open(device_num)
        return v_cam

    def get_channel_sum(self, image, channel_num):
        channels = cv2.split(image)
        sum = cv2.sumElems(channels[channel_num])
        return sum[0]

    def detect_face(self, image):
        faces = self.face.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60), maxSize=(250, 250))
        if len(faces) > 0:
            strt_x = faces[0][0]
            strt_y = faces[0][1]
            width = faces[0][2]
            height = faces[0][3]
            only_face = image[strt_y:strt_y+height, strt_x:strt_x+width]
            return only_face
        return image

    def detect_skin(selfself, face, background):
        min_YCrCb = np.array([0,133,77],np.uint8)
        max_YCrCb = np.array([255,173,127],np.uint8)

        imageYCrCb = cv2.cvtColor(face,cv2.COLOR_BGR2YCR_CB)
        skinRegion = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)
        skin = cv2.bitwise_and(face, face, mask=skinRegion)
        image, contours, hierarchy = cv2.findContours(skinRegion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i, c in enumerate(contours):
            area = cv2.contourArea(c)
            if area > 2000:
                cv2.drawContours(face, contours, i, (0, 255, 0), 3)
                masked_img = face.copy()
                cv2.fillPoly(face, contours, [0, 0, 0])
                face = masked_img - face

        return face
                



imProc = ImageProcessor(0.01)
cam = imProc.camera_open(0)
while True:

    bla, image = cam.read()
    face = imProc.detect_face(image)
    skin = imProc.detect_skin(face, image)
    cv2.imshow("skin", skin)
    cv2.waitKey(10)






# @asyncio.coroutine
# def periodic(camera):
#     #while len(imProc.result_array)<4:
#      while True:
#         bla, image = camera.read()
#         face = imProc.detect_face(image)
#         cv2.imshow("image", face)
#         im_integral = imProc.get_channel_sum(face, 2)
#         cv2.waitKey(1)
#         yield from asyncio.sleep(imProc.discrete_period)
#
# def stop():
#     print("blea")
#     task.cancel()
#
# cam = imProc.camera_open(0)
# task = asyncio.Task(periodic(cam))
# loop = asyncio.get_event_loop()
#
# try:
#     loop.run_until_complete(task)
# except asyncio.CancelledError as e:
#     pass
#
# print(imProc.result_array)