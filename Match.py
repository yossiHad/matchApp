from threading import Lock
import threading
from Chat import ChatManager
from Player import Player
import sys


class MatchManager:
    CODE_LENGTH = 3
    HEADER = 3
    MATCH_FOUND = b"#01"
    CANCEL_REQUEST_MESSAGE = b"#02"
    lock = Lock()

    def __init__(self):
        self.games = {}
        self.chat_manager = ChatManager()

    def register_game(self, player, game_name):
        print("[MATCH] entering register_game")
        if game_name not in self.games.keys():
            self.games[game_name] = [player]
        else:
            self.games[game_name].append(player)
        thread = self.start(player)
        thread.start()
        thread.join()

    def start(self, player):
        print("[MATCH] entering start")
        thread_search = threading.Thread(target=self.wait_room, args=(player,))
        thread_cancel = threading.Thread(target=self.cancel_message, args=(player,))
        thread_cancel.daemon = True
        thread_search.start()
        thread_cancel.start()
        while thread_search.is_alive() and thread_cancel.is_alive():
            pass
        print("out of loop")
        if thread_search.is_alive():
            print("[MATCH] player ", player.get_name(), " have canceled the request")
            return threading.Thread(target=self.nothing)
        else:
            print("[MATCH] player ", player.get_name(), " is in chat!")
            return threading.Thread(target=self.chatting, args=(player,))
        sys.exit()

    def chatting(self, player):
        print(f"[MATCH] player {player.get_name()} chatting")
        chatting = True
        while chatting:
            chatting = player.in_chat
        print(f"[MATCH] player {player.get_name()} end chatting")

    def nothing(self):
        print("[MATCH] enter nothing")
        pass

    def match_searching(self):
        while True:
            self.lock.acquire()
            games = self.games.keys()
            for game in games:
                game_players = self.games[game]
                if len(game_players) > 1:
                    player1 = game_players.pop(0)
                    player2 = game_players.pop(0)
                    print(f"player {player1.get_name()} in match with player {player2.get_name()}")
                    self.notify(player1, player2)
                    self.notify(player2, player1)
                    self.chat_manager.init_chat(player1, player2)
            self.lock.release()

    def remove(self, game_name, player_socket):
        self.games[game_name].remove(player_socket)
        if len(self.games[game_name]) == 0:
            del self.games[game_name]

    def pad(self, string:str):
        return str(len(string)).ljust(self.HEADER, ' ').encode()

    def notify(self, player1, player2):
        print(f"[MATCH] notifying player {player1.get_name()}")
        player1.set_in_chat(True)
        player1_socket = player1.get_socket()
        player2_name = player2.get_name()
        player1_socket.send(self.MATCH_FOUND + self.pad(player2_name) + player2_name.encode())

    def wait_room(self, player):
        print(f"[MATCH] player {player.get_name()} is in wait room")
        chatting = False
        while not chatting:
            chatting = player.in_chat
        print(f"[MATCH] player {player.get_name()} get out of the wait room")

    def cancel_message(self, player):
        print(f"[MATCH] player {player.get_name()} is in cancel_message")
        player_socket = player.get_socket()
        msg_code = player_socket.recv(self.CODE_LENGTH)
        print("[MATCH] msg_code is: ", msg_code)
        if msg_code == self.CANCEL_REQUEST_MESSAGE:
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            self.games[player.game].remove(player)
            if not self.games[player.game]:
                del self.games[player.game]
            player_socket.send(self.CANCEL_REQUEST_MESSAGE)
            player.reset_game()
        else:
            pass
        print(f"[MATCH] player {player.get_name()} is out of cancel_message")


