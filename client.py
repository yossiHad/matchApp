import socket
import threading

HEADER = 64
PORT = 1236
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send():
    i = 0
    while i < 2:
        msg = input()
        if msg == "12":
            message = msg
        else:
            send = msg[2:]
            # message = msg.encode(FORMAT)
            msg_length = len(send)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            message = msg[:2] + send_length.decode() + msg[2:]
            # client.send(send_length)
        message = message.encode()
        client.send(message)


def receive():
    while True:
        msg_length = int(client.recv(2).decode())
        msg =""
        if msg_length != 11:
            msg = client.recv(msg_length).decode()
        print(f"message length:{msg_length}, msg:{msg}")


thread_send = threading.Thread(target=send)
thread_recv = threading.Thread(target=receive)
thread_send.start()
thread_recv.start()

"""send(DISCONNECT_MESSAGE)"""

