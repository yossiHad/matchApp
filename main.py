import threading
import time
from threading import Lock
from asyncio.windows_events import NULL
import multiprocessing

import socket
lock = threading.Lock()
d = {}

def inter():
    i = 0
    for x in range(10):
        d[x] = []
    while True:


        for x in range(i):
            d[i].append(x)
        i = i + 1

        if i == 10:
            i=0
        #     for x in range(i):
        #         if x != 0:
        #             d[x].remove(x - 1)
        #     i = 0

def remove():
    i = 0
    while True:
        for x in range(i):
            if x != 0:
                d[x].remove(x - 1)
                d[x].append(x-1)
        i = i + 1
        if i == 10:
            i = 0


# lock = Lock()
# threading.Thread(target=allways).start()
# threading.Thread(target=inter).start()
# threading.Thread(target=remove).start()

def count():
    for i in range(10):
        print(str(i))


# thread1 = threading.Thread(target=count)
# thread1.daemon = True
# thread1.start()

def recv():
    try:
        print("inside recv")
        data = client.recv(4).decode()
        print("finish recv ", data)
    except Exception as e:
        print(e)

def send():
    client.send(input().encode())


def input_player():
    print("inside input")
    input()
    print("finish input")

def init_thread(func):
    return threading.Thread(target=func)

HEADER = 3
PORT = 1237
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
def thread():
    thread1 = init_thread(recv)
    thread1.daemon = True
    thread1.start()

    thread2 = threading.Thread(target=count)
    thread2.daemon = True
    thread2.start()

    while thread1.is_alive() and thread2.is_alive():
        pass

def all(list, i):
    lock.acquire()
    while 1 not in list:
        time.sleep(3)
        list.append(i)
        print(list)
    lock.release()

def count2(list):
    while True:
        time.sleep(5)
        list.append(2)
        print(list)

list = []
# threading.Thread(target=all,args=(list, 0)).start()

if __name__ == '__main__':
    thread1 = threading.Thread(target=all, args=(list, 1))
    thread2 = threading.Thread(target=send)
    thread2.start()
    print("sfgfgsfdgsdfgfgfg")
    process = multiprocessing.Process(target=recv)
    thread1.start()
    print("ghgggggggggggggggggggggggggggggggggggggggggggggggg")
    process.start()
    print("Addddddddddddddddddd")
    while process.is_alive() and thread1.is_alive():
        print("in")
        time.sleep(10)
        list.append(1)
    # process.terminate()

#process.terminate()

