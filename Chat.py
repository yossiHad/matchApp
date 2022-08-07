import threading
import time

from Player import Player


class ChatManager:

    def __init__(self):
        self.players_chats = {}

    def init_chat(self, player1, player2):
        print("[CHAT] init_chat")
        chat = Chat(player1, player2)
        chat.start()


class Chat:
    MESSAGE_SENT = b"#10"
    LEAVE_CHAT = b"#11"
    CONFIRMATION_MESSAGE = b"#04"
    HEADER = 3
    CODE_LENGTH = 3

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def start(self):
        print("[CHAT] starting chat thread")
        thread_player1 = self.init_thread(self.player1, self.player2)
        thread_player2 = self.init_thread(self.player2, self.player1)
        thread_player1.start()
        thread_player2.start()
        while thread_player1.is_alive() or thread_player2.is_alive():
            time.sleep(2)
            print("##################################################################################################")
            pass
        thread_player1.join()
        thread_player2.join()

    def init_thread(self, player1, player2):
        thread = threading.Thread(target=self.chat, args=(player1, player2))
        return thread

    def chat(self, player1, player2):
        print(f"[CHAT] player {player1.get_name()} chatting with player {player2.get_name()}")
        player1_socket = player1.get_socket()
        player2_socket = player2.get_socket()
        while player1.in_chat and player2.in_chat:
            try:
                msg_code = player1_socket.recv(self.CODE_LENGTH)
                print(player1.get_name(),"@@@@@@@@@@@@@@@@@@@")
                print("[CHAT] after receive msg_code player: ", player1.get_name())
                if msg_code:
                    if msg_code == self.LEAVE_CHAT:
                        self.end_chat(player2_socket)
                    elif msg_code == self.CONFIRMATION_MESSAGE:
                        print("jfgijdfigjidfjgifdgj out of chat")
                    else:
                        msg_length = int(player1_socket.recv(self.HEADER).decode())
                        msg = player1_socket.recv(msg_length).decode()
                        if msg_code == self.MESSAGE_SENT:
                            player2_socket.send(self.MESSAGE_SENT + self.pad(msg) + msg.encode())
                        else:
                            pass

            except Exception as e:
                print("[CHAT]error for player:", player1.get_name(), " is:", e)
                self.end_chat(player2_socket)
        print(f"[CHAT] player {player1.get_name()} end chatting with player {player2.get_name()}")

    def pad(self, string:str):
        return str(len(string)).ljust(self.HEADER, ' ').encode()

    def end_chat(self, player_socket):
        self.player1.set_in_chat(False)
        self.player2.set_in_chat(False)
        self.player1.reset_game()
        self.player2.reset_game()
        player_socket.send(self.LEAVE_CHAT)
