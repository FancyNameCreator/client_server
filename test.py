# subprocess.call(['python somescript.py'])
import base64
import json
import pickle
import subprocess
import time
from io import BytesIO

from PIL import Image

import cv2

proc = subprocess.Popen("python test_sub.py", stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# while True:
#     bytes_ = proc.stdout.readline()
#         # proc.communicate()
#         # proc.stdout.readline()
#     # print(len(bytes_))
#
#     load = json.loads(bytes_)
#     imdata = base64.b64decode(load['image1'])
#     im = pickle.loads(imdata)
#
#     cv2.imshow("img", im)

bytes_ = proc.stdout.readline()
        # proc.communicate()
        # proc.stdout.readline()
    # print(len(bytes_))

load = json.loads(bytes_)
imdata = base64.b64decode(load['image'])
im = Image.open(BytesIO(imdata))
im.show()

# cv2.imshow("img", im)

time.sleep(15)



# --------------- RECEIVER
# load = json.loads(bytes_)
# imdata = base64.b64decode(load['image'])
# im = Image.open(BytesIO(imdata))
# im.show()

# --------------- SENDER
# picture = cv2.imread("pic.jpg")
# _, imdata = cv2.imencode('.JPG', picture)
# jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})
