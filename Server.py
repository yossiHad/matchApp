import socket
import threading
from Match import MatchManager
from Clients import *
from Chat import ChatManager

HEADER = 3
PORT = 1237
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


class ServerManager:
    USERNAME_MESSAGE = "#00"
    GAME_NAME_MESSAGE = "#01"
    CANCLE_REQUEST_MESSGAE = "#03"
    MESSAGE_SENT = "#10"
    LEAVE_CHAT = "#11"
    CODE_LENGTH = 3



    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.clients_games = {}
        self.match_manager = MatchManager()
        thread_match_search = threading.Thread(target=self.match_manager.match_searching)
        thread_match_search.start()
        self.Players_manager = PlayersManagerSingleton.get_instance()


    def handle_client(self,player_socket, addr):
        connected = True
        try:
            while connected:
                msg_code = player_socket.recv(self.CODE_LENGTH).decode()
                if msg_code:
                    if msg_code == self.LEAVE_CHAT:
                        if player_socket in self.clients_games.keys():
                            player2_socket = self.Players_manager.get_opponent_socket(player_socket)
                            player2_socket.send(self.DISCONNECT_MESSAGE.encode())
                            self.end_match(player_socket)
                        else:
                            pass
                            # TODO decide what to do if trying to leave non-exist chat
                    else:
                        msg_length = int(player_socket.recv(HEADER).decode())
                        msg = player_socket.recv(msg_length).decode()
                        if msg_code == self.MESSAGE_SENT:
                            if player_socket in self.Players_manager.players_in_chat():
                                player2_socket = self.Players_manager.get_opponent_socket()
                                player2_socket.send(self.MESSAGE_SENT.encode() + self.pad(msg) + msg.encode())
                            else:
                                pass
                                #TODO decide what to do if trying to send a message while not connected to chat

                        elif msg_code == self.GAME_NAME_MESSAGE:
                            self.clients_games[player_socket] = msg
                            self.match_manager.register_game(player_socket,msg)
                        elif msg_code == self.CANCLE_REQUEST_MESSGAE:
                            if player_socket in self.clients_games.keys():
                                player_socket.send(self.CANCLE_REQUEST_MESSGAE.encode())
                                game_name = self.clients_games[player_socket]
                                self.match_manager.remove(game_name,player_socket)
                                del self.clients_games[player_socket]
                            else:
                                pass
                                #TODO need to decide what to do if the client asks to cancle a non-exist request
        except:
            pass



    def register(self,player_socket):
        try:
            msg_code = player_socket.recv(self.CODE_LENGTH).decode()
            username_length = int(player_socket.recv(HEADER).decode())
            username = player_socket.recv(username_length).decode()
            self.Players_manager.add_client(player_socket,username)
            return True
        except:
            return False


    def enter_client(self,player_socket,addr):
        if self.register(player_socket):
            self.handle_client(player_socket,addr)

    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread_enter = threading.Thread(target=self.enter_client,args=(conn,addr))
            thread_enter.start()

    def end_match(self,player_socket):
        player2_socket = self.Players_manager.get_opponent_socket(player_socket)
        del self.clients_games[player_socket]
        del self.clients_games[player2_socket]
        self.Players_manager.remove_player(player_socket)
        self.Players_manager.remove_player(player2_socket)

    def pad(self, string: str):
        return str(len(string)).ljust(self.HEADER, ' ').encode()


#starting the server
server = ServerManager()
server.start()