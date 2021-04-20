import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
BUFFER_SIZE = 8

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept()
print(f"[+] {address} is connected.")

received = bytearray()

while True:
    bytes_read = client_socket.recv(BUFFER_SIZE)
    if not bytes_read:
        break
    else:
        received += bytes_read

str_ = received.decode()

print(str_)

client_socket.close()
s.close()
