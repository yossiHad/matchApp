import threading
import socket



HEADER = 3
PORT = 1237
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


class ServerTest:
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


    def register(self, player_socket):
        msg_code = player_socket.recv(self.CODE_LENGTH).decode()
        print(msg_code)
        player_socket.send(b'1234')
        print("af")

        # username_length = int(player_socket.recv(HEADER).decode())
        # username = player_socket.recv(username_length).decode()
        # player = Player(username, player_socket)
        # self.Players_manager.add_player(player)
        # return player


    def enter_client(self, player_socket):
        try:
            player = self.register(player_socket)
            self.handle_client(player)
        except:
            print("!2312312312122132132")


    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread_enter = threading.Thread(target=self.enter_client, args=(conn,))
            thread_enter.start()

se=ServerTest()
se.start()