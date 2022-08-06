import threading
from threading import Lock
from asyncio.windows_events import NULL
from queue import Empty


d = {}
def allways():
    while True:
        lock.acquire()

        for key in d.keys():
            print("key:",key," val:",d[key])
        lock.release()
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

d = {}
d[1] = 1
d[2] = 2
print(d)
list = list(d.values())
list.append(3)
print(list)
print(d.values())