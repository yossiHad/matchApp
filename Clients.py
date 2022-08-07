from Chat import ChatManager
from Player import Player

class PlayersManager:
    players_dict = {}


    def __init__(self):
        self.players = {}


    def add_player(self,player):
        player_socket = player.get_socket()
        self.players[player_socket] = player

    def get_opponent_socket(self,player_socket):
        return self.players_dict[player_socket]

    def remove_player(self,player_socket):
        del self.players_dict[player_socket]

    def players_in_chat(self):
        return self.players_dict.keys()

    def get_player(self,player_socket):
        if player_socket in self.players.keys():
            return self.players[player_socket]


class PlayersManagerSingleton:
    Players_manager = PlayersManager()

    def get_instance(self):
        return self.Players_manager