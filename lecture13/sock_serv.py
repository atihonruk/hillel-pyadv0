from socket import *
from threading import Thread

from concurrent.futures import ProcessPoolExecutor # ThreadPoolExecutor


process_pool = ProcessPoolExecutor(4)


# 1, 1, 2, 3, 5, 8,  
def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n - 2) + fib(n - 1)


def fib_handler(client):
    with client:
        while True:
            data = client.recv(256) # blocking
            if not data:
                break
            arg = int(data)
            fut = process_pool.submit(fib, arg)
            res = fut.result() 
            # res = fib(arg)
            client.sendall((str(res) + '\n').encode())
 

def serve_forever(handle_connection, addr='127.0.0.1', port=5000):
    # Python 3.8
    # with create_server((addr, port)) as sock:  # AF_INET, SOCK_STREAM)
    with socket() as sock:
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((addr, port))
        sock.listen()  # backlog)
        print(f'Listening {addr}:{port}')
        while True:
            client, (addr, port) = sock.accept()  # blocking
            print(f'Connected from {addr}:{port}')
            Thread(target=handle_connection, args=(client,)).start()
 

if __name__ == '__main__':
    serve_forever(fib_handler)
