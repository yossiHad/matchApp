from Chat import ChatManager

class PlayersManager:
    players_dict = {}


    def __init__(self):
        self.clients = {}
        

    def add_client(self,player_socket, username):
        self.clients[player_socket] = username

    def get_opponent_socket(self,player_socket):
        return self.players_dict[player_socket]

    def remove_player(self,player_socket):
        del self.players_dict[player_socket]

    def players_in_chat(self):
        return self.players_dict.keys()



class PlayersManagerSingleton:
    Players_manager = PlayersManager()

    def get_instance(self):
        return self.Players_manager