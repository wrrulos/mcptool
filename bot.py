import socket
import threading

class handle_server(threading.Thread):
    def __init__(self,client_socket,target_host, target_port,target_socket):
        super().__init__()
        self.client_socket = client_socket
        self.target_host = target_host
        self.target_port = target_port
        self.target_socket = target_socket
    def run(self):
        client_socket = self.client_socket
        target_host   = self.target_host
        target_port   = self.target_port
        target_socket = self.target_socket
        while True:
            data = client_socket.recv(4096 * 8 * 8 * 8)
            if len(data) == 0:
                print("Client connection closed.")
                break
            print(f'Received from server: {data}')
            target_socket.send(data)
            print("Sent to target.")

        client_socket.close()
        target_socket.close()


class handle_client_Thread(threading.Thread):
    def __init__(self,client_socket,target_host, target_port,target_socket):
        self.client_socket = client_socket
        self.target_host = target_host
        self.target_port = target_port
        self.target_socket = target_socket
        super().__init__()
    def run(self):
        client_socket = self.client_socket
        target_host   = self.target_host
        target_port   = self.target_port
        target_socket = self.target_socket
        while True:
            response = target_socket.recv(4096 * 8 * 8 * 8)
            if len(response) == 0:
                print("Target connection closed.")
                break
            print(f'Received from client: {response}')
            client_socket.send(response)
            print("Sent to client.")

        client_socket.close()
        target_socket.close()

def handle_client(client_socket, target_host, target_port):
    # Connect to the target server
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))
    handle_server(client_socket, target_host, target_port,target_socket).start()
    handle_client_Thread(client_socket, target_host, target_port,target_socket).start()

def start_proxy(proxy_port, target_host, target_port):
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', proxy_port))
    server_socket.listen(5)
    print(f'Proxy server listening on port {proxy_port}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Accepted connection from {addr[0]}:{addr[1]}')
        client_handler = threading.Thread(
            target=handle_client,
            args=(client_socket, target_host, target_port)
        )
        client_handler.start()


# Usage example
proxy_port = 55555
target_host = "158.69.52.203"
target_port = 25565

start_proxy(proxy_port, target_host, target_port)