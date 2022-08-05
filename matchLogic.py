import socket
import threading
from threading import Lock
import time

HEADER = 64
PORT = 1236
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

CODE_LENGTH = 2


players_dict = {}

class ServerManager:
    USERNAME_MESSAGE = "00"
    GAME_NAME_MESSAGE = "01"
    CANCLE_REQUEST_MESSGAE = "03"
    MESSAGE_SENT = "10"
    DISCONNECT_MESSAGE = "11"
    LEAVE_CHAT = "12"

    def __init__(self):
        print("[STARTING] starting the server...")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.clients = {}
        self.clients_games = {}
        self.match_manager = MatchManager()
        thread_match_search = threading.Thread(target=self.match_manager.match_searching)
        thread_match_search.start()


    def handle_client(self,player_socket, addr):
        print(f"[NEW CONNECTION] {addr} connected")
        connected = True
        while connected:
            print("start loop")
            msg_code = player_socket.recv(CODE_LENGTH).decode()
            if msg_code:
                if msg_code == self.DISCONNECT_MESSAGE:
                    print(f"[SERVER] disconnecting from connection {addr}")
                    connected = False
                elif msg_code == self.LEAVE_CHAT:
                    if player_socket in self.clients_games.keys():
                        player2_socket = players_dict[player_socket]
                        player2_socket.send(self.DISCONNECT_MESSAGE.encode())
                        self.end_match(player_socket)
                        print("ending match!")
                    else:
                        pass
                        # TODO decide what to do if trying to leave non-exist chat
                else:
                    print("[SERVER] entering...")
                    msg_length = int(player_socket.recv(HEADER).decode())
                    msg = player_socket.recv(msg_length).decode()
                    if msg_code == self.MESSAGE_SENT:
                        if player_socket in players_dict.keys():
                            player2_socket = players_dict[player_socket]
                            player2_socket.send(str(msg_length).encode() + msg.encode())
                        else:
                            pass
                            #TODO decide what to do if trying to send a message while not connected to chat

                    elif msg_code == self.GAME_NAME_MESSAGE:
                        print("[SERVER] passing game to play")
                        self.clients_games[player_socket] = msg
                        self.match_manager.register_game(player_socket,msg)
                    elif msg_code == self.CANCLE_REQUEST_MESSGAE:
                        print("[SERVER] canceling request")
                        if player_socket in self.clients_games.keys():
                            game_name = self.clients_games[player_socket]
                            self.match_manager.remove(game_name,player_socket)
                            del self.clients_games[player_socket]
                        else:
                            pass
                            #TODO need to decide what to do if the client asks to cancle a non-exist request

        player_socket.close()


    def register(self,player_socket):
        msg_code = player_socket.recv(CODE_LENGTH).decode()
        username_length = int(player_socket.recv(HEADER).decode())
        username = player_socket.recv(username_length).decode()
        self.clients[player_socket] = username


    def enter_client(self,player_socket,addr):
        self.register(player_socket)
        self.handle_client(player_socket,addr)

    def start(self):
        self.server.listen()
        print(f"[LISTENING] server is listening on {SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread_enter = threading.Thread(target=self.enter_client,args=(conn,addr))
            thread_enter.start()

    def end_match(self,player_socket):
        player2_socket = players_dict[player_socket]
        del self.clients_games[player_socket]
        del self.clients_games[player2_socket]
        del players_dict[player_socket]
        del players_dict[player2_socket]


class MatchManager:
    MATCH_FOUND = "01"
    lock = Lock()
    def __init__(self):
        self.games = {}
        self.stop = False

    def register_game(self,player_entering_socket, game_name):
        print(f"[MATCHMANAGER] registering new player to the game - {game_name}")
        if game_name not in self.games.keys():
            self.games[game_name] = [player_entering_socket]
        else:
            self.games[game_name].append(player_entering_socket)


    def match_searching(self):
        while True:
            self.lock.acquire()
            for game in self.games.values():
                if len(game) > 1:
                    print("[MATCHMANAGER] match between two players")
                    player1_socket = game.pop(0)
                    player2_socket = game.pop(0)
                    player1_socket.send(self.MATCH_FOUND.encode())
                    player2_socket.send(self.MATCH_FOUND.encode())
                    players_dict[player1_socket] = player2_socket
                    players_dict[player2_socket] = player1_socket
            self.lock.release()

    def remove(self,game_name,player_socket):
        self.games[game_name].remove(player_socket)
        if len(self.games[game_name]) == 0:
            del self.games[game_name]



server = ServerManager()
server.start()