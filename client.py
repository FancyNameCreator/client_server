import socket
import os

BUFFER_SIZE = 8
host = "127.0.0.1"
port = 5001

s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

bytes_ = "....................................................................".encode()
counter = 0

while True:
    if len(bytes_) - counter < 0:
        print("breaking")
        break

    if len(bytes_) - (counter + BUFFER_SIZE) < 0:
        to_be_send = bytes_[counter:]
        s.sendall(to_be_send)
        print(f"sending bytes from {counter} to {counter + (len(bytes_) - counter)}")
    else:
        to_be_send = bytes_[counter:(counter+BUFFER_SIZE)]
        s.sendall(to_be_send)
        print(f"sending bytes from {counter} to {counter + BUFFER_SIZE}")

    counter += BUFFER_SIZE

s.close()
