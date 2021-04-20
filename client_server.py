import base64
import json
import socket
import threading
import time
import asyncio
from io import BytesIO

import cv2
from PIL import Image


class Client:
    BUFFER_SIZE = 32768
    is_free = True
    host = "127.0.0.1"
    port = 5002

    def __init__(self):
        self.s = socket.socket()
        print(f"[+] Connecting to {self.host}:{self.port}")
        self.s.connect((self.host, self.port))
        print("[+] Connected.")

    def __del__(self):
        self.s.close()

    def send_bytes(self, bytes_):
        if not self.is_free:
            return
        self.is_free = False

        self.s.sendall(str(len(bytes_)).encode())
        print(f"Bytes_ length is {len(bytes_)}")
        print(f"Size of size encoded {len(str(len(bytes_)).encode())}")

        _counter = 0

        while True:
            if len(bytes_) - _counter < 0:
                print("breaking")
                break

            if len(bytes_) - (_counter + self.BUFFER_SIZE) < 0:
                to_be_send = bytes_[_counter:]
                self.s.sendall(to_be_send)
                print(f"sending bytes from {_counter} to {_counter + (len(bytes_) - _counter)}")
            else:
                to_be_send = bytes_[_counter:(_counter + self.BUFFER_SIZE)]
                self.s.sendall(to_be_send)
                print(f"sending bytes from {_counter} to {_counter + self.BUFFER_SIZE}")

            _counter += self.BUFFER_SIZE

        confirmation = self.s.recv(6)
        print(f"received confirmation: {confirmation}")
        print("message should be sent now, changing status")
        self.is_free = True


class Server:
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 5002
    BUFFER_SIZE = 32768

    def __init__(self):
        self.s = socket.socket()
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.s.listen(5)
        print(f"[*] Listening as {self.SERVER_HOST}:{self.SERVER_PORT}")

        self.client_socket = None
        self.address = None
        self.receive()

    def __del__(self):
        self.client_socket.close()
        self.s.close()

    def receive(self):
        while True:
            self.client_socket, self.address = self.s.accept()
            print(f"[+] {self.address} is connected.")

            try:
                while True:
                    bytes_to_read_length = int(self.client_socket.recv(6).decode())
                    print(bytes_to_read_length)
                    received = bytearray()

                    while True:
                        bytes_read = self.client_socket.recv(self.BUFFER_SIZE)
                        if not bytes_read or len(received) >= bytes_to_read_length:
                            print("breaking")
                            break
                        else:
                            received.extend(bytes_read)
                            print(f"appending {bytes_read.decode()}, received length so far {len(received)}")

                        if len(received) >= bytes_to_read_length:
                            print("breaking")
                            break

                    print("before decode")
                    # str_ = received.decode()

                    load = json.loads(received.decode())
                    imdata = base64.b64decode(load['image'])
                    im = Image.open(BytesIO(imdata))
                    im.show()

                    # print(str_)
                    print(f"str length {len(received)}")

                    self.client_socket.sendall(str(len(received)).encode())
                    # received = bytearray()
            except Exception as e:
                print(e)
                print("Client disconnected")


def thread(client_: Client, name, time_):
    try:
        while True:
            print(f"thread {name}")
            # test(client_)
            client_.send_bytes("....................................................................".encode())
            time.sleep(time_)
            print(client_.is_free)
    except KeyboardInterrupt:
        print("shutting down")


if __name__ == '__main__':
    client = Client()

    # x = threading.Thread(target=thread(client, "x", 2.2), args=(1,))
    # y = threading.Thread(target=thread(client, "y", 3.3), args=(1,))
    # x.start()
    # y.start()

    picture = cv2.imread("pic.jpg")
    _, imdata = cv2.imencode('.JPG', picture)
    jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})

    try:
        while True:
            print("main")
            # test(client)
            client.send_bytes(jstr.encode())
            time.sleep(2)
            print(client.is_free)
    except KeyboardInterrupt:
        print("shutting down")
