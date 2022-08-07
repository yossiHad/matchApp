import socket
import threading
from Match import MatchManager
from Player import Player


class ServerManager:
    HEADER = 3
    PORT = 1237
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)

    USERNAME_MESSAGE = b"#00"
    GAME_NAME_MESSAGE = b"#01"
    CANCEL_REQUEST_MESSAGE = b"#02"
    MESSAGE_SENT = b"#10"
    LEAVE_CHAT = b"#11"
    CODE_LENGTH = 3

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.match_manager = MatchManager()
        thread_match_search = threading.Thread(target=self.match_manager.match_searching)
        thread_match_search.start()

    def handle_client(self, player):
        print("entering handle client")
        connected = True
        player_socket = player.get_socket()
        try:
            while connected:
                print("start loop")
                msg_code = player_socket.recv(self.CODE_LENGTH).decode()
                print("the msg_code is: ", msg_code)
                print("after receiving")
                if msg_code:
                    print("in condition")
                    msg_length = int(player_socket.recv(self.HEADER).decode())
                    msg = player_socket.recv(msg_length).decode()
                    print("after getting full message")
                    if msg_code.encode() == self.GAME_NAME_MESSAGE:
                        print("[SERVER] entering game set")
                        player.set_game(msg)
                        self.match_manager.register_game(player, msg)
                        print("[SERVER] exit register_game")
                        print("[SERVER] player ",player.get_name(), " is in chat? ", player.in_chat)
                        print("[SERVER] player ", player.get_name(), "game is: ", player.game)
                    else:
                        pass
        except Exception as e:
            print("error ", e)

    def register(self,player_socket):
        msg_code = player_socket.recv(self.CODE_LENGTH).decode()
        username_length = int(player_socket.recv(self.HEADER).decode())
        username = player_socket.recv(username_length).decode()
        player = Player(username, player_socket)
        return player

    def enter_client(self,player_socket):
        try:
            player = self.register(player_socket)
            self.handle_client(player)
        except:
            pass

    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread_enter = threading.Thread(target=self.enter_client,args=(conn,))
            thread_enter.start()

    def pad(self, string: str):
        return str(len(string)).ljust(self.HEADER, ' ').encode()


# starting the server
server = ServerManager()
server.start()