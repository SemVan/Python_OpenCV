import cv2
import asyncio


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
    return sum[0]



result_array = []
discrete_period = 1/20

@asyncio.coroutine
def periodic(camera):
    while len(result_array)<4:
        bla, image = camera.read()
        blue, green, red = cv2.split(image)
        result_array.append(get_image_sum(green))
        yield from asyncio.sleep(discrete_period)

def stop():
    print("blea")
    task.cancel()

cam = camera_open(0)
task = asyncio.Task(periodic(cam))
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(task)
except asyncio.CancelledError as e:
    pass

print(result_array)