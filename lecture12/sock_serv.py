from socket import *


def echo_handler(client):
    while True:
        data = client.recv(256)
        if not data:
            break
        client.sendall(data)
 

def serve_forever(handle_connection, addr='127.0.0.1', port=5000):
    # Python 3.8
    with create_server((addr, port)) as sock:  # AF_INET, SOCK_STREAM)
        # sock.bind((addr, port))
        # sock.listen()  # backlog)
        print(f'Listening {addr}:{port}')
        while True:
            client, (addr, port) = sock.accept()  # blocking
            with client:
                print(f'Connected from {addr}:{port}')
                handle_connection(client)
 

if __name__ == '__main__':
    serve_forever(echo_handler)
