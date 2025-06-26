import socket
import threading

HOST = '192.168.1.11'
PORT = 5051

clients = []

def broadcast(msg, source=None):
    for client in clients[:]:
        try:
            client.sendall(msg)
        except:
            clients.remove(client)

def handle_client(conn, addr):

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            msg = f" {data.decode('utf-8')}"
            broadcast(msg.encode('utf-8'), conn)
        except:
            break
    clients.remove(conn)
    conn.close()
    print(f"[Ngắt kết nối] {addr}")

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #// Cho phép tái sử dụng địa chỉ cổng
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server chat đang chạy tại {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        print(f"[Kết nối mới] {addr}")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()








