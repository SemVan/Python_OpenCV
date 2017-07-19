import cv2
import asyncio


class Image_processor:

    def __init__(self, period):
        self.face = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        self.result_array = []
        self.discrete_period = period
        return

    def  camera_open(self, device_num):
        v_cam = cv2.VideoCapture(device_num)
        v_cam.open(device_num)
        return v_cam

    def get_image_sum(self, image):
        sum = cv2.sumElems(image)
        return sum[0]

    def detect_face(self, image):
        faces = self.face.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), maxSize=(250,250))
        if len(faces) > 0:
            strt_x = faces[0][0]
            strt_y = faces[0][1]
            width = faces[0][2]
            height = faces[0][3]
            only_face = image[strt_y:strt_y+height, strt_x:strt_x+width]
            return only_face
        return image


imProc = Image_processor(0.01)
# cam = imProc.camera_open(0)
# bla, image = cam.read()
# face = imProc.detect_face(image)
#
# if len(face)>0:
#     strt_x = face[0][0]
#     strt_y = face[0][1]
#     width = face[0][2]
#     height = face[0][3]
#     cv2.rectangle(image, (strt_x, strt_y),(strt_x+width, strt_y+height), (255,0,0), 2)
#
# cv2.imshow("image", image)
# cv2.waitKey()
# cam.close()
# print(len(face))
#
# cv2.rectangle(image, (face[0], face[1]),(face[2], face[3]))

@asyncio.coroutine
def periodic(camera):
    #while len(imProc.result_array)<4:
     while True:
        bla, image = camera.read()
        face = imProc.detect_face(image)
        cv2.imshow("image", face)
        #blue, green, red = cv2.split(image)
        #imProc.result_array.append(imProc.get_image_sum(green))
        cv2.waitKey(1)
        yield from asyncio.sleep(imProc.discrete_period)

def stop():
    print("blea")
    task.cancel()

cam = imProc.camera_open(0)
task = asyncio.Task(periodic(cam))
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(task)
except asyncio.CancelledError as e:
    pass

print(imProc.result_array)