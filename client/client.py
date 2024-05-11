import socket

def communicate_with_server(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 12345))

        client_socket.send(request.encode())

        response = client_socket.recv(1024).decode()
        print("Server response:", response)

communicate_with_server("ADD_GROUP Group_1")
communicate_with_server("ADD_STUDENT Student_1 1")
