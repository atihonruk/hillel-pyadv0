from socket import *


with socket() as sock:
    sock.connect(('127.0.0.1', 5000))
    sock.sendall('Hello, Python'.encode())
    data = sock.recv(256)
    print(data.decode())
