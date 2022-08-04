import socket
import threading
import time

HEADER = 64
PORT = 1236
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

CODE_LENGTH = 2

DISCONNECT_MESSAGE = "11"


class ServerManager:
    USERNAME_MESSAGE = "00"
    GAME_NAME_MESSAGE = "01"
    CANCLE_REQUEST_MESSGAE = "03"
    in_chat = False

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
        i = 0
        connected = True
        while connected:
            if i < 1:
                msg_code = player_socket.recv(CODE_LENGTH).decode()
                if msg_code:
                    if msg_code == DISCONNECT_MESSAGE:
                        print(f"[SERVER] disconnecting from connection {addr}")
                        connected = False
                    else:
                        print("[SERVER] entering...")
                        msg_length = int(player_socket.recv(HEADER).decode())
                        msg = player_socket.recv(msg_length).decode()
                        if msg_code == self.GAME_NAME_MESSAGE:
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
                # i = i +1
                
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


class MatchManager:

    def __init__(self):
        self.games = {}
        self.stop = False
        self.iter = 0

    def register_game(self,player_entering_socket, game_name):
        print(f"[MATCHMANAGER] registering new player to the game - {game_name}")
        if game_name not in self.games.keys():
            self.games[game_name] = [player_entering_socket]
        else:
            self.games[game_name].append(player_entering_socket)
            if self.iter == 0:
                player1.in_chat = True
                self.iter = self.iter + 1
            else:
                player2.in_chat = True
            """
            players_list = self.games[game_name]
            player_wait_socket = players_list.pop(0)
            chat = Chat(player_entering_socket,player_wait_socket)
            """



    def match_searching(self):
        while True:
            if self.stop:
                time.sleep(0.03)
            for game in self.games.values():
                while len(game) > 1:
                    print("[MATCHMANAGER] match between two players")
                    player1_socket = game.pop(0)
                    player2_socket = game.pop(0)
                    chat = Chat(player1_socket,player2_socket)
                    thread = threading.Thread(target=chat.start)
                    thread.start()

    
    def remove(self,game_name,player_socket):
        self.stop = True
        time.sleep(0.01)
        self.games[game_name].remove(player_socket)
        if len(self.games[game_name]) == 0:
            del self.games[game_name]
        self.stop = False


class Chat:

    MESSAGE_SENT = "10"
    MATCH_FOUND = "01"
    LEAVE_CHAT = "11"


    def __init__(self, player1_socket, player2_socket):
        self.player1_socket = player1_socket
        self.player2_socket = player2_socket
        self.notify()
        ServerManager.in_chat = True
    
    
    def notify(self):
        match_msg = self.MATCH_FOUND.encode()
        self.player1_socket.send(match_msg)
        self.player2_socket.send(match_msg)


    def chat(self,player_from_socket, player_to_socket):
        print("[CHAT] start chating")
        connected_to_chat = True
        while connected_to_chat:
            msg_code = player_from_socket.recv(CODE_LENGTH).decode()
            if msg_code == self.LEAVE_CHAT:
                connected_to_chat = False
                player_to_socket.send(self.LEAVE_CHAT.encode())
            elif msg_code != self.MESSAGE_SENT:
                msg_length = int(player_from_socket.recv(HEADER).decode())
                msg = player_from_socket.recv(msg_length)
                #TODO to send the code,size protocol
                msg_length = f"{str(msg_length):<2}"
                msg = msg_code.encode() + msg_length.encode() + msg
                player_to_socket.send(msg)
            else:
                pass
                #TODO need to check what to do if we are getting  msg_code we dont familiar with




    def start(self):
        thread1 = threading.Thread(target=self.chat,args=(self.player1_socket,self.player2_socket))
        thread2 = threading.Thread(target=self.chat,args=(self.player2_socket,self.player1_socket))
        # self.chat(self.player1_socket,self.player2_socket)
        # self.chat(self.player2_socket,self.player1_socket)
        thread1.start()
        thread2.start()



class player1:
    in_chat = False


class player2:
    in_chat = False



server = ServerManager()
server.start()