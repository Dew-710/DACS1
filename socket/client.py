import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "192.168.0.123"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    response = client.recv(2048).decode(FORMAT)
    print(f"Response from server: {response}")


while True:
    msg = input("Send Something: ")
    if msg.strip() == "":
        send(DISCONNECT_MESSAGE)
        client.close()
        print("Disconnected from server.")
        break
    send(msg)
