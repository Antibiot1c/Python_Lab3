import socket
import sqlite3

conn = sqlite3.connect('server/database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
                    group_id INTEGER PRIMARY KEY,
                    group_name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    student_name TEXT,
                    group_id INTEGER,
                    FOREIGN KEY(group_id) REFERENCES groups(group_id))''')

def handle_client_request(client_socket, request):
    parts = request.split(" ")
    operation = parts[0].strip()
    
    if operation == "ADD_GROUP":
        group_name = parts[1].strip()
        add_group(group_name)
        client_socket.send("Group added successfully".encode())
    elif operation == "ADD_STUDENT":
        student_name = parts[1].strip()
        group_id = int(parts[2].strip())
        add_student(student_name, group_id)
        client_socket.send("Student added successfully".encode())
    else:
        client_socket.send("Invalid operation".encode())

def add_group(group_name):
    cursor.execute('INSERT INTO groups (group_name) VALUES (?)', (group_name,))
    conn.commit()
    print(f"Group '{group_name}' added successfully.")

def add_student(student_name, group_id):
    cursor.execute('INSERT INTO students (student_name, group_id) VALUES (?, ?)', (student_name, group_id))
    conn.commit()
    print(f"Student '{student_name}' added to group {group_id} successfully.")

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 12345))
        server_socket.listen()

        print("Server is running on localhost:12345")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            request = client_socket.recv(1024).decode()
            print(f"Received request from client: {request}")

            handle_client_request(client_socket, request)

            client_socket.close()

# Виклик функції для запуску сервера
if __name__ == "__main__":
    run_server()
