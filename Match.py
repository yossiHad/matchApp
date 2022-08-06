from Server import ServerManager
from threading import Lock


class MatchManager:
    HEADER = 3
    MATCH_FOUND = "#01"
    lock = Lock()

    def __init__(self):
        self.games = {}

    def register_game(self,player_entering_socket, game_name):
        if game_name not in self.games.keys():
            self.games[game_name] = [player_entering_socket]
        else:
            self.games[game_name].append(player_entering_socket)

    def match_searching(self):
        while True:
            self.lock.acquire()
            games = self.games.values()
            for game in games:
                if len(game) > 1:
                    player1_socket = game.pop(0)
                    player2_socket = game.pop(0)
                    player1_name = ServerManager.clients[player1_socket]
                    player2_name = ServerManager.clients[player2_socket]
                    player1_socket.send(self.MATCH_FOUND.encode() + self.pad(player1_name) + player1_name.encode())
                    player2_socket.send(self.MATCH_FOUND.encode() + self.pad(player2_name) + player2_name.encode())
                    ServerManager.players_dict[player1_socket] = player2_socket
                    ServerManager.players_dict[player2_socket] = player1_socket
            self.lock.release()

    def remove(self,game_name,player_socket):
        self.games[game_name].remove(player_socket)
        if len(self.games[game_name]) == 0:
            del self.games[game_name]

    def pad(self, string:str):
        return str(len(string)).ljust(self.HEADER,' ').encode()
