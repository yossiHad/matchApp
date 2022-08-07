import socket
import threading

HEADER = 3
PORT = 1237
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
        if msg == "#02":
            message = msg
        else:
            send = msg[3:]
            # message = msg.encode(FORMAT)
            msg_length = len(send)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            message = msg[:3] + send_length.decode() + msg[3:]
            # client.send(send_length)
        print("before")
        message = message.encode()
        print("after")
        client.send(message)


def receive():
    while True:
        print("enter")
        msg = client.recv(3).decode()

        print("first msf is: ", msg)
        msg_length = int(client.recv(HEADER).decode())
        print("after read")
        msg =""
        if msg_length != 11:
            print("try read")
            msg = client.recv(msg_length).decode()
            print("after msg read")
        print(f"message length:{msg_length}, msg:{msg}")
        if msg == "#01":
            client.send("#01".encode())


thread_send = threading.Thread(target=send)
thread_recv = threading.Thread(target=receive)
thread_send.start()
thread_recv.start()

"""send(DISCONNECT_MESSAGE)"""

