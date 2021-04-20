import base64
import json
import pickle
import time
import cv2
import sys
from client_server import Server


def main():
    picture = cv2.imread("pic.jpg")
    # print(cv2.imencode(".jpg", picture)[1])

    # imdata = pickle.dumps(picture)
    # jstr = json.dumps(
    #     {
    #         "image1": base64.b64encode(imdata).decode('ascii'),
    #         "image2": base64.b64encode(imdata).decode('ascii')
    #     })

    _, imdata = cv2.imencode('.JPG', picture)
    jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})

    # json_objects_dict = json.dumps(jstr, indent=4).encode()

    while True:
        # print("running")
        # sys.stdout.buffer.write(json_objects_dict)
        # sys.stdout.write(jstr)
        # sys.stdout.writelines(jstr)
        # sys.stdout.flush()
        print(jstr)
        # sys.stdout.flush()
        time.sleep(3)


if __name__ == '__main__':
    Server()
    # main()
